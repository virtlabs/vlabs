import yaml
from vlabs import AppManager
from creation import Provision
from volumes import Vol


class Var:
    def __init__(self):
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)
        self.namespace = 'test-project'

    def buildvar(self, inputvar):
        if 'pvc' in inputvar:
            pvc = True
        else:
            pvc = False

        var = {}
        q = int(inputvar['appindex'])
        var[str(inputvar['nameoftheapp'])] = {}
        print(pvc)
        # INPUT
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            var[str(inputvar['nameoftheapp'])][j] = {}
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                for key in inputvar:
                    if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name'] == key:
                        var[str(inputvar['nameoftheapp'])][j][str(key)] = str(inputvar[key])

        # VARIABLE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'variable':
                    for k in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                        if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['service'] == \
                                self.ysrvc['marketplace']['apps'][q]['services'][k]['nameservice']:
                            for l in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][k]['env'])):
                                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['variable'] == \
                                        self.ysrvc['marketplace']['apps'][q]['services'][k]['env'][l]['name']:
                                    var[str(inputvar['nameoftheapp'])][j][
                                        self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = \
                                        var[str(inputvar['nameoftheapp'])][k][
                                            self.ysrvc['marketplace']['apps'][q]['services'][k]['env'][l]['name']]

        # SERVICE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'service':
                    for k in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                        if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['service'] == \
                                self.ysrvc['marketplace']['apps'][q]['services'][k]['nameservice']:
                            idname = str(inputvar['nameoftheapp']) + "-" + \
                                     self.ysrvc['marketplace']['apps'][q]['services'][j]['nameservice']
                            var[str(inputvar['nameoftheapp'])][j][
                                self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = str(
                                inputvar['nameoftheapp']) + "-" + \
                                                                                                         self.ysrvc[
                                                                                                             'marketplace'][
                                                                                                             'apps'][q][
                                                                                                             'services'][
                                                                                                             k][
                                                                                                             'nameservice']

                            # static
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'static':
                    var[str(inputvar['nameoftheapp'])][j][
                        self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = \
                        self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['value']
        # ROUTE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'route':
                    var[str(inputvar['nameoftheapp'])][j][
                        self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = "http://" + idname + \
                                                                                                 self.ysrvc['domain']
        print(var)
        self.create(q, str(inputvar['nameoftheapp']), var, pvc)

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
            envvar = var[nameapp][j]
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
