import kubernetes.config as kconf
import kubernetes.client
import yaml
from kubernetes.client.rest import ApiException
import openshift.client
import openshift.config as oconf
from creation import Provision
from deletion import Del
from volumes import Vol
from openshift.client.models import V1DeploymentConfigList, V1DeploymentConfig, V1Route
from openshift.client.models.v1_route_list import V1RouteList

# kubernetes.config.load_kube_config()
kcfg = kconf.new_client_from_config()
ocfg = oconf.new_client_from_config()


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

    def getenv(self, index):
        varuser = []
        vardesc = []
        q = int(index)
        D = {}
        try:
            for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
                for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                    if '$input' in self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['value']:
                        varuser.append(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name'])
                        vardesc.append(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['description'])
            D = dict(zip(varuser, vardesc))

        except:
            print("app non esistente")
        D['appindex'] = q
        return D

class AppManager:
    def __init__(self, namespace):
        self.namespace = namespace
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

    def getrunning(self):
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        timeout_seconds = 56
        try:
            api_response = api_instance.list_namespaced_service(self.namespace, pretty='true',
                                                                timeout_seconds=timeout_seconds)
            itemslist = api_response.items
            y = len(itemslist)
            name = []
            for x in range(0, y):
                if 'gluster.kubernetes.io/provisioned-for-pvc' in itemslist[x].metadata.labels:
                    pass
                else:
                    name.append(itemslist[x].metadata.name)
            return name

        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_services: %s\n" % e)

    def create(self, app):
        # try:

        nameapp = raw_input("Inserisci il nome della tua applicazione: ")
        app_index = next(index for (index, d) in enumerate(self.ysrvc['marketplace']['apps']) if d["name"] == app)
        service = self.ysrvc['marketplace']['apps'][app_index]['name']
        for j in range(0, len(self.ysrvc['marketplace']['apps'][app_index]['services'])):
            deploy = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['nameservice']
            imagename = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['imagename']
            port = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['ports']
            envvar = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['env']

            psvc = Provision()
            psvc.createsvc(deploy, port, imagename, self.namespace, envvar, nameapp, service)



            # except:
            #    print("app non esistente")

    def delete(self, lbl):
        #lbl = 'label=' + dellabel
        bundle = lbl.split("=")[1]
        dcs = self.listdc(lbl)
        svcs = self.listsvc(lbl)
        rts = self.listroute(lbl)
        rcs = self.listrcs(lbl)
        print(lbl, bundle, dcs, svcs, rcs)

        dd = Del()
        dd.delrt(rts, self.namespace, ocfg)
        dd.delsvc(svcs, self.namespace, kcfg)
        dd.deldc(dcs, self.namespace, ocfg)
        dd.setrc(rcs, self.namespace, kcfg)
        dd.delrc(rcs, self.namespace, kcfg)

    def listdcnosel(self):
        api_del = openshift.client.OapiApi(ocfg)
        namespace = self.namespace
        pretty = 'true'
        timeout_seconds = 5

        try:
            api_response = api_del.list_namespaced_deployment_config(namespace, pretty=pretty,
                                                                     timeout_seconds=timeout_seconds)
            dcs = []

            for h in range(0, len(api_response.items)):
                dcs.append(api_response.items[h].metadata.name)
            return dcs

        except ApiException as e:
            print("Exception when calling OapiApi->list_namespaced_deployment_config: %s\n" % e)

    def listdc(self, dcsel):
        api_del = openshift.client.OapiApi(ocfg)
        namespace = self.namespace
        pretty = 'true'
        timeout_seconds = 5

        try:
            api_response = api_del.list_namespaced_deployment_config(namespace, pretty=pretty, label_selector=dcsel,
                                                                     timeout_seconds=timeout_seconds)
            dcs = []

            for h in range(0, len(api_response.items)):
                dcs.append(api_response.items[h].metadata.name)
            return dcs

        except ApiException as e:
            print("Exception when calling OapiApi->list_namespaced_deployment_config: %s\n" % e)

    def listsvc(self, svcsel):
        # listsvc by selector
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        namespace = self.namespace
        pretty = 'true'
        timeout_seconds = 5

        try:
            api_response = api_instance.list_namespaced_service(namespace, pretty=pretty,
                                                                label_selector=svcsel, timeout_seconds=timeout_seconds)
            svcs = []
            for h in range(0, len(api_response.items)):
                svcs.append(api_response.items[h].metadata.name)
            return svcs


        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_service: %s\n" % e)

    def listroute(self, rtsel):
        api_instance = openshift.client.OapiApi(ocfg)
        namespace = self.namespace
        timeout_seconds = 5
        api_response = V1RouteList()

        try:
            api_response = api_instance.list_namespaced_route(namespace, pretty='true', label_selector=rtsel,
                                                              timeout_seconds=timeout_seconds)
            rts = []
            for h in range(0, len(api_response.items)):
                rts.append(api_response.items[h].metadata.name)
            return rts

        except ApiException as e:
            print("Exception when calling OapiApi->list_namespaced_route: %s\n" % e)

    def listrcs(self, rcsel):
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        namespace = self.namespace
        timeout_seconds = 5

        try:
            api_response = api_instance.list_namespaced_replication_controller(namespace, pretty='true',
                                                                               label_selector=rcsel,
                                                                               timeout_seconds=timeout_seconds)
            rcs = []
            for h in range(0, len(api_response.items)):
                rcs.append(api_response.items[h].metadata.name)
            return rcs
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_replication_controller: %s\n" % e)

    def readroute(self, sel):
        api_instance = openshift.client.OapiApi(ocfg)
        namespace = self.namespace
        timeout_seconds = 5
        api_response = V1Route()
        try:
            api_response = api_instance.list_namespaced_route(namespace, label_selector=sel, pretty='true')
            spek = api_response
            rtalias = []
            for i in range(0, len(spek.items)):
                rtalias.append(spek.items[i].spec.host)
            print(rtalias)
            return rtalias

        except ApiException as e:
            print("Exception when calling OapiApi->list_namespaced_route: %s\n" % e)

    def svcstatus(self, name):
        api_instance = kubernetes.client.CoreV1Api(kcfg)

        try:
            api_response = api_instance.read_namespaced_service(name, self.namespace, pretty='true')
            return api_response.metadata.creation_timestamp
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service_status: %s\n" % e)

    def getrunbundleenv(self, singlesvc):
        api_instance = openshift.client.OapiApi(ocfg)
        serviceenv = []
        try:
            for i in range(0, len(singlesvc)):
                api_response = api_instance.read_namespaced_deployment_config(singlesvc[i], self.namespace, pretty='true')
                serviceenv.append(api_response.spec.template.spec.containers[0].env)
                senv = dict(zip(singlesvc, serviceenv))
            return senv
        except ApiException as e:
                print("Exception when calling OapiApi->read_namespaced_deployment_config: %s\n" % e)

    def getbundle(self, name):
        api_instance = kubernetes.client.CoreV1Api(kcfg)

        try:
            api_response = api_instance.read_namespaced_service(name, self.namespace, pretty='true')
            sel = api_response.metadata.labels
            if 'bundle' in sel:
                selector = 'bundle=' + sel['bundle']
            elif 'app' in sel:
                selector = 'app=' + sel['app']
            print(selector)
            return selector

        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service_status: %s\n" % e)
