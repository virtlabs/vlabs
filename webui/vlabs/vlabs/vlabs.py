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
import subprocess
import shlex
from pprint import pprint

#config_file = '/root/.kube/' + str(sessionid) + '.config'
#kcfg = kconf.new_client_from_config()
#ocfg = oconf.new_client_from_config()
###

class Auth:
    def __init__(self, sessionid):
        self.pathcfg = self.cfg_file = '/root/.kube/' + str(sessionid) + '.config'
        print("CREO OGGETTO CLASSE AUTH")
        print(str(sessionid))
        print(self.pathcfg)
        print("FINE CONTROLLO CLASSE AUTH - INIT -")

    def login(self, user, pwd):
        ccrp = ['oc', 'login', 'https://openshift#########', '-u', str(user), '-p', str(pwd),
         '--insecure-skip-tls-verify=true', '--config=' + self.pathcfg]
        check = subprocess.call(ccrp)
        return check

    def logout(self):
        rmfl = ['rm', str(self.pathcfg)]
        check = subprocess.call(rmfl)
        return check

    def chooseprj(self):
        self.ocfg = oconf.new_client_from_config(self.pathcfg)
        api_instance = openshift.client.OapiApi(self.ocfg)
        try:
            list = api_instance.list_project(pretty='true')
            prjs = []
            for i in range(0, len(list.items)):
                prjs.append(list.items[i].metadata.name)
            return prjs
        except ApiException as e:
            print("Exception when calling OapiApi->list_project: %s\n" % e)


class AppManager:
    def __init__(self, namespace, user=None):
        config_file = '/root/.kube/' + user + '.config'
        self.namespace = namespace
        self.stream = file('vlabs_template.yml', 'r')
        self.ysrvc = yaml.load(self.stream)
        self.kcfg = kconf.new_client_from_config(config_file)
        self.ocfg = oconf.new_client_from_config(config_file)


    def users(self, *args):
        api_instance = openshift.client.UserOpenshiftIoV1Api(self.ocfg)
        try:
            utenti = api_instance.list_user()
            if args:
                return utenti
            else:
                return True
        except ApiException:
            return False

    def rolebinding(self, ns):
        api_instance = openshift.client.AuthorizationOpenshiftIoV1Api(self.ocfg)
        timeout_seconds = 56

        try:
            api_response = api_instance.list_namespaced_role_binding(ns, timeout_seconds=timeout_seconds)
            return api_response
        except ApiException as e:
            print("Exception when calling AuthorizationOpenshiftIoV1Api->list_namespaced_role_binding: %s\n" % e)

    def getpvpvcs(self, ns):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
        try:
            api_response = api_instance.list_namespaced_persistent_volume_claim(ns, timeout_seconds=timeout_seconds)
            print("PVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVC")
            print(api_response)
            print("PVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVCPVPVC")
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_persistent_volume_claim: %s\n" % e)


    def getrunningadmin(self, ns):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56

        try:
            api_response = api_instance.list_namespaced_service(ns, pretty='true',
                                                                timeout_seconds=timeout_seconds)
            itemslist = api_response.items
            y = len(itemslist)
            name = []
            for x in range(0, len(itemslist)):
                if itemslist[x].metadata.labels and 'bundle' in itemslist[x].metadata.labels:
                    name.append(itemslist[x].metadata.name)
            return name
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_services: %s\n" % e)

    def getrunning(self, *args):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56

        try:
            api_response = api_instance.list_namespaced_service(self.namespace, pretty='true',
                                                                timeout_seconds=timeout_seconds)
            itemslist = api_response.items
            ### y = len(itemslist) to erase
            if args:
                dictbundle = {}
                for x in range(0, len(itemslist)):
                    if itemslist[x].metadata.labels and 'bundle' in itemslist[x].metadata.labels:
                        if itemslist[x].metadata.labels['bundle'] in dictbundle.keys():
                            dictbundle[itemslist[x].metadata.labels['bundle']].append(itemslist[x].metadata.name)
                        else:
                            dictbundle[itemslist[x].metadata.labels['bundle']] = []
                            dictbundle[itemslist[x].metadata.labels['bundle']].append(itemslist[x].metadata.name)
                print("ITEMSLIIIIIIIIIIIIIIIIIIIIIST")
                print(dictbundle)
                return dictbundle
            else:
                name = []
                for x in range(0, len(itemslist)):
                    if itemslist[x].metadata.labels and 'bundle' in itemslist[x].metadata.labels:
                        name.append(itemslist[x].metadata.name)
                #    pass
                #else:
                #name.append(itemslist[x].metadata.name)
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
        dd.delrt(rts, self.namespace, self.ocfg)
        dd.delsvc(svcs, self.namespace, self.kcfg)
        dd.deldc(dcs, self.namespace, self.ocfg)
        dd.setrc(rcs, self.namespace, self.kcfg)
        dd.delrc(rcs, self.namespace, self.kcfg)

    def listdcnosel(self):
        api_del = openshift.client.OapiApi(self.ocfg)
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
        api_del = openshift.client.OapiApi(self.ocfg)
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
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
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
        api_instance = openshift.client.OapiApi(self.ocfg)
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
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
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
        api_instance = openshift.client.OapiApi(self.ocfg)
        namespace = self.namespace
        timeout_seconds = 5
        spek = V1Route()
        try:
            spek = api_instance.list_namespaced_route(namespace, label_selector=sel, pretty='true')
            rtalias = []
            for i in range(0, len(spek.items)):
                rtalias.append(spek.items[i].spec.host)
            print(rtalias)
            return rtalias

        except ApiException as e:
            print("Exception when calling OapiApi->list_namespaced_route: %s\n" % e)

    def svctime(self, name):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)

        try:
            api_response = api_instance.read_namespaced_service(name, self.namespace, pretty='true')
            return api_response.metadata.creation_timestamp
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service_status: %s\n" % e)

    def svcstatus(self, name):
        api_instance = openshift.client.OapiApi(self.ocfg)

        try:
            api_response = api_instance.read_namespaced_deployment_config_status(name, self.namespace, pretty='true')
            cond = api_response.status.conditions
            if cond[0].last_transition_time > cond[1].last_transition_time:
                activecond = cond[0].type
            else:
                activecond = cond[1].type
############################SISTEMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            return cond[0].status
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service_status: %s\n" % e)

    def getrunbundleenv(self, singlesvc):
        api_instance = openshift.client.OapiApi(self.ocfg)
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
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)

        try:
            api_response = api_instance.read_namespaced_service(name, self.namespace, pretty='true')
            sel = api_response.metadata.labels
            selector = 'bundle=' + sel['bundle']
            return selector

        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_service_status: %s\n" % e)

    def patchdcvar(self, name, namespace, body):
        api_instance = openshift.client.OapiApi(self.ocfg)
        try:
            api_response = api_instance.patch_namespaced_deployment_config(name, namespace, body, pretty='true')
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling OapiApi->patch_namespaced_deployment_config: %s\n" % e)

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

        for j in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'])):
            if self.ysrvc['marketplace']['apps'][q]['services'][j]['env']:
                for i in range(0, len(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'])):
                    if '$input' in self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['value']:
                        varuser.append(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['name'])
                        vardesc.append(self.ysrvc['marketplace']['apps'][q]['services'][j]['env'][i]['description'])
        D = dict(zip(varuser, vardesc))
        D['appindex'] = q
        return D