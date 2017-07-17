import kubernetes.config
import kubernetes.client
from pprint import pprint
import yaml
import time
from kubernetes.client.rest import ApiException
import openshift.client

from creation import Provision
from deletion import Del

kubernetes.config.load_kube_config()


class Config:
    def __init__(self):
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

    def getready(self):
        pass

    def getmarket(self):
        for j in range(0, len(self.ysrvc['marketplace']['apps'])):
            print(self.ysrvc['marketplace']['apps'][j]['name'])

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
        '''
        for j in range(0, len(self.ysrvc['marketplace'])):
            self.srvc = self.ysrvc['marketplace'][j]
            print(self.srvc['env'])
        '''
        # print(self.ysrvc['marketplace']['moodle']['imagename'])


class AppManager:
    def __init__(self, namespace):
        self.namespace = namespace
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

    def getrunning(self):
        api_instance = kubernetes.client.CoreV1Api()
        timeout_seconds = 56
        try:
            api_response = api_instance.list_namespaced_service(self.namespace, pretty='true',
                                                                timeout_seconds=timeout_seconds)
            itemslist = api_response.items
            y = len(itemslist)
            for x in range(0, y):
                name = itemslist[x].metadata.name
                print(name)
                x += 1

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

    def delete(self, dellabel):
        dcs = self.listdc(dellabel)
        svcs = self.listsvc(dellabel)
        rts = self.listroute(dellabel)
        rcs = self.listrcs(dellabel)

        dd = Del()
        dd.delrt(rts, self.namespace)
        dd.delsvc(svcs, self.namespace)
        dd.deldc(dcs, self.namespace)
        dd.setrc(rcs, self.namespace)
        dd.delrc(rcs, self.namespace)


    def listdc(self, dcsel):
        api_del = openshift.client.OapiApi()
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
        api_instance = kubernetes.client.CoreV1Api()
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
        api_instance = openshift.client.OapiApi()
        namespace = self.namespace
        timeout_seconds = 5  # int | Timeout for the list/watch call. (optional)

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
        api_instance = kubernetes.client.CoreV1Api()
        namespace = self.namespace
        include_uninitialized = 'true'
        timeout_seconds = 5
        # watch = true  # bool | Watch for changes to the described resources and return them as a stream of add,
        # update, and remove notifications. Specify resourceVersion. (optional)

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


