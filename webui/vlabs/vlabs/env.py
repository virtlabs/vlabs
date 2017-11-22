import yaml
from vlabs import AppManager
from creation import Provision
from volumes import Vol
import re


class Var:
    def __init__(self, namespace):
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)
        self.domain = str(self.ysrvc['domain'])
        self.namespace = namespace

    def envregex(self, total):
        print('ENVREGEX-total')
        print(total)
        m = re.findall(r"((\$.*?)\[(.*?)\])", total)
        return m


    def buildvar(self, inputvar):
        if 'pvc' in inputvar:
            pvc = True
        else:
            pvc = False

        var = {}
        q = int(inputvar['appindex'])
        app = str(inputvar['nameoftheapp'])
        var[app] = {}

        print('INPUTVAR')
        print(inputvar)

        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            svc = self.ysrvc['marketplace']['apps'][q]['services'][j]['nameservice']
            #idname = str(inputvar['nameoftheapp']) + '-' + svc
            var[app][svc] = {}
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                var[app][svc][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['value']
                if "$input" in var[app][svc][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']]:
                    inp = str(var[app][svc][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']])
                    inp2 = inp.replace("$input", inputvar[self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']])
                    var[app][svc][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = inp2
                else:
                    pass

        ev = ('$service', '$route', '$variable')
        for k in var[app]:
            for l in var[app][k]:
                if any(x in var[app][k][l] for x in ev):
                    group = self.envregex(var[app][k][l])
                    for g in range(0, len(group)):
                        if group[g][1] == '$service':
                            repl = var[app][k][l].replace(str(group[g][0]), str(app + "-" + group[g][2]))
                            var[app][k][l] = repl
                        if group[g][1] == '$route':
                            for p in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                                if self.ysrvc['marketplace']['apps'][q]['services'][p]['nameservice'] == group[g][2].split(":")[0]:
                                    for portsarray in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][p]['ports'])):
                                        if self.ysrvc['marketplace']['apps'][q]['services'][p]['ports'][portsarray]['port'] == group[g][2].split(":")[1]:
                                            idname = str(app + "-" + self.ysrvc['marketplace']['apps'][q]['services'][p]['nameservice'])
                                            repl = var[app][k][l].replace(str(group[g][0]), "http://" + idname + '-' + str(portsarray) + str(self.ysrvc['domain']))
                                            var[app][k][l] = repl
                        if group[g][1] == '$variable':
                            rightvar = var[app][group[g][2].split(":")[0]][group[g][2].split(":")[1]]
                            repl = var[app][k][l].replace(group[g][0], rightvar)
                            var[app][k][l] = repl
            print(var[app][k])

        self.create(q, app, var, pvc)

    def create(self, app_index, nameapp, var, pvc=None):
        pv = Vol()
        volumename = None
        datadir = None
        # app_index = next(index for (index, d) in enumerate(self.ysrvc['marketplace']['apps']) if d["name"] == app)
        service = self.ysrvc['marketplace']['apps'][app_index]['name']
        for j in range(0, len(self.ysrvc['marketplace']['apps'][app_index]['services'])):
            deploy = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['nameservice']
            imagename = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['imagename']
            port = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['ports']
            envvar = var[nameapp][deploy]
            psvc = Provision()

            if pvc:
                if self.ysrvc['marketplace']['apps'][app_index]['services'][j]['volumes']['persistentvolumeclaim'] == 'yes':
                    datadir = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['volumes']['datadir']
                    pv.createvolume(nameapp, deploy, datadir)
                    volumename = pv.pvc(nameapp, deploy)
                else:
                    pass
            else:
                pass

            psvc.createsvc(deploy, port, imagename, self.namespace, envvar, nameapp, service, pvc, volumename, datadir)

