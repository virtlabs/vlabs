from django.http import HttpResponse
import yaml
from file import Prova

def hello(request):
    #return HttpResponse("Hello world") 
    mao = Config()
    ma = mao.getmarket()
    print(ma)
    html = "<html><body>Market %s.</body></html>" % ma
    return HttpResponse(html)


class Config:
    def __init__(self):
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

    def getready(self):
        pass

    def getmarket(self):
        mk = []
        for j in range(0, len(self.ysrvc['marketplace']['apps'])):
            mk.append(self.ysrvc['marketplace']['apps'][j]['name'])
        return mk

    def load(self):
        pass

    def appinfo(self, app):
        try:
            app_index = next(index for (index, d) in enumerate(self.ysrvc['marketplace']['apps']) if d["name"] == app)
            print(self.ysrvc['marketplace']['apps'][app_index])
        except:
            print("app non esistente")

    def getports(self, app):
        try:
            app_index = next(index for (index, d) in enumerate(self.ysrvc['marketplace']['apps']) if d["name"] == app)
            for j in range(0, len(self.ysrvc['marketplace']['apps'][app_index]['services'])):
                print(self.ysrvc['marketplace']['apps'][app_index]['services'][j]['nameservice'])
                print(self.ysrvc['marketplace']['apps'][app_index]['services'][j]['ports'])
                print("\n")
        except:
            print("app non esistente")

    def getenv(self, app):
        pass

