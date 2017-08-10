import yaml


class Var:
    def __init__(self):
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

    def buildvar(self, inputvar):
        var = {}
        q = int(inputvar['appindex'])
        var[str(inputvar['nameoftheapp'])] = {}
        # INPUT
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            var[str(inputvar['nameoftheapp'])][j] = {}
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                for key in inputvar:
                    if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name'] == key:
                        var[str(inputvar['nameoftheapp'])][j][str(key)] = str(inputvar[key])
        print(var)
        # VARIABLE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'variable':
                    for k in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                        if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['service'] == self.ysrvc['marketplace']['apps'][q]['services'][k]['nameservice']:
                            var[str(inputvar['nameoftheapp'])][j][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = var[str(inputvar['nameoftheapp'])][k][self.ysrvc['marketplace']['apps'][q]['services'][k]['env'][i]['name']]
                            # la var devo prenderla in k e salvarla in j
                            pass
                    pass
        print(var)
        # SERVICE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'service':
                    for k in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                        if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['service'] == self.ysrvc['marketplace']['apps'][q]['services'][k]['nameservice']:
                            idname = str(inputvar['nameoftheapp']) + "-" + self.ysrvc['marketplace']['apps'][q]['services'][j]['nameservice']
                            var[str(inputvar['nameoftheapp'])][j][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = idname
        print(var)
        # static
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'static':
                    var[str(inputvar['nameoftheapp'])][j][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['value']
        # ROUTE
        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                if self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['type'] == 'route':
                    var[str(inputvar['nameoftheapp'])][j][self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name']] = "http://" + idname + self.ysrvc['domain']
        print(var)

