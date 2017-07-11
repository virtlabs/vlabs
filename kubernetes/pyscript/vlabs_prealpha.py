import kubernetes.config
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
import yaml
import time
from kubernetes.client.rest import ApiException
from kubernetes import config, client
from pprint import pprint
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_pod_spec import V1PodSpec
import kubernetes.client.models
import openshift.client
import openshift.client.models

kubernetes.config.load_kube_config()


class Config:
    def __init__(self):
        self.stream = file('yaml_alpha.yml', 'r')
        self.ysrvc = yaml.load(self.stream)

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
        self.stream = file('y2.yml', 'r')
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
        app_index = next(index for (index, d) in enumerate(self.ysrvc['marketplace']['apps']) if d["name"] == app)
        service = self.ysrvc['marketplace']['apps'][app_index]['name']
        for j in range(0, len(self.ysrvc['marketplace']['apps'][app_index]['services'])):
            deploy = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['nameservice']
            imagename = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['imagename']
            port = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['ports']
            envvar = self.ysrvc['marketplace']['apps'][app_index]['services'][j]['env']

            psvc = Provision()
            psvc.createsvc(service, deploy, port, imagename, self.namespace, envvar)


            # except:
            #    print("app non esistente")

    def delete(self):
        pass


class Provision:
    def __init__(self):
        config.load_kube_config()
        self.o1 = openshift.client.OapiApi()
        self.k1 = kubernetes.client.CoreV1Api()

    def createsvc(self, service, deploy, port, imagename, namespace, envvar):
        bservice = client.V1Service()
        smeta = V1ObjectMeta()
        dcmeta = V1ObjectMeta()
        pmt = V1ObjectMeta()
        sspec = client.V1ServiceSpec()
        bdc = openshift.client.V1DeploymentConfig()
        dcspec = openshift.client.V1DeploymentConfigSpec()

        strategy = openshift.client.V1DeploymentStrategy()
        rollingparams = openshift.client.V1RollingDeploymentStrategyParams()
        podtemp = client.V1PodTemplateSpec()
        podspec = client.V1PodSpec()
        container = client.V1Container()

        smeta.name = service+deploy   ###############################EJELO! occhio qui!
        smeta.namespace = namespace
        smeta.labels = {namespace: deploy}  # podlabel

        sspec.selector = {namespace: deploy}  # podlabel
        sspec.ports = []

        for l in range(0, len(port)):
            p = client.V1ServicePort()
            p.name = "{port}-{tcp}".format(**port[l])
            p.protocol = "TCP"
            p.port = port[l]['tcp']
            p.target_port = "{port}-{tcp}".format(**port[l])
            sspec.ports.append(p)
            if port[l]['route'] == 'yes':
                sd=service+deploy
                self.createroute(p.target_port, sd, deploy, namespace)
                continue




        bservice.api_version = 'v1'
        bservice.kind = 'Service'
        bservice.metadata = smeta
        bservice.spec = sspec
        bservice.api_version = 'v1'

        # DeploymentConfig

        dcmeta.labels = {namespace: deploy}
        dcmeta.name = deploy
        dcmeta.namespace = namespace

        rollingparams.interval_seconds = 1

        strategy.labels = {namespace: deploy}
        strategy.type = 'Rolling'
        strategy.rolling_params = rollingparams

        container.image = imagename
        container.name = deploy
        container.env = []

        for key in envvar:
            v = client.V1EnvVar()
            v.name = key
            v.value = envvar[key]
            container.env.append(v)

        container.ports = []
        for o in range(0, len(port)):
            p = client.V1ContainerPort()
            p.name = ("{port}-{tcp}".format(**port[o]))
            p.protocol = "TCP"
            p.container_port = port[l]['tcp']
            container.ports.append(p)

        pmt.labels = {namespace: deploy}
        pmt.name = deploy

        podspec.containers = [container]

        podtemp.metadata = pmt
        podtemp.spec = podspec

        dcspec.replicas = 2
        dcspec.selector = {namespace: deploy}
        dcspec.template = podtemp
        dcspec.strategy = strategy

        bdc.api_version = 'v1'
        bdc.spec = dcspec
        bdc.metadata = dcmeta
        bdc.kind = 'DeploymentConfig'

        try:
            self.k1.create_namespaced_service(namespace=namespace, body=bservice, pretty='true')
        except ApiException as e:
            print("Exception when calling OapiApi->create_service: %s\n" % e)

        try:
            self.o1.create_namespaced_deployment_config(namespace=namespace, body=bdc, pretty='true')
        except ApiException as e:
            print("Exception when calling OapiApi->create_dc: %s\n" % e)

    def createroute(self, target, service, deploy, namespace):
        rbody = openshift.client.V1Route()
        routemeta = V1ObjectMeta()
        routespec = openshift.client.V1RouteSpec()
        routeport = openshift.client.V1RoutePort()
        routeto = openshift.client.V1RouteTargetReference()

        routeport.target_port = target
        routeto.kind = 'Service'
        routeto.name = service
        routeto.weight = 100

        routespec.host = service + '[address].it'
        routespec.port = routeport
        routespec.to = routeto

        routemeta.labels = {namespace: deploy}
        routemeta.name = service
        routemeta.namespace = namespace

        rbody.api_version = 'v1'
        rbody.kind = 'Route'
        rbody.metadata = routemeta
        rbody.spec = routespec

        try:
            self.o1.create_namespaced_route(namespace=namespace, body=rbody, pretty='true')
        
        except ApiException as e:
            print("Exception when calling OapiApi->create_route: %s\n" % e)
 
  
