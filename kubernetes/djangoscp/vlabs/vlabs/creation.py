from kubernetes import config, client
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
import openshift.client.models
import kubernetes.client.models
import openshift.client
from kubernetes.client.rest import ApiException


class Provision:
    def __init__(self):
        config.load_kube_config()
        self.o1 = openshift.client.OapiApi()
        self.k1 = kubernetes.client.CoreV1Api()

    def createsvc(self, deploy, port, imagename, namespace, envvar, nameapp, service):
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

        idname = nameapp + "-" + deploy

        smeta.name = idname   # !!!
        smeta.namespace = namespace
        smeta.labels = {"label": idname, "bundle": service + "-" + nameapp}

        sspec.selector = {"label": idname}
        sspec.ports = []

        for l in range(0, len(port)):
            p = client.V1ServicePort()
            p.name = "{port}-{tcp}".format(**port[l])
            p.protocol = "TCP"
            p.port = port[l]['tcp']
            p.target_port = "{port}-{tcp}".format(**port[l])
            sspec.ports.append(p)
            if port[l]['route'] == 'yes':
                self.createroute(p.target_port, idname, namespace, service, nameapp)
                continue

        bservice.api_version = 'v1'
        bservice.kind = 'Service'
        bservice.metadata = smeta
        bservice.spec = sspec
        bservice.api_version = 'v1'

        # DeploymentConfig

        dcmeta.labels = {"label": idname, "bundle": service + "-" + nameapp}
        dcmeta.name = idname
        dcmeta.namespace = namespace

        rollingparams.interval_seconds = 1

        strategy.labels = {"label": idname, "bundle": service + "-" + nameapp}
        strategy.type = 'Rolling'
        strategy.rolling_params = rollingparams

        container.image = imagename
        container.name = idname
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
            p.container_port = port[o]['tcp']
            container.ports.append(p)

        pmt.labels = {"label": idname, "bundle": service + "-" + nameapp}
        pmt.name = idname

        podspec.containers = [container]

        podtemp.metadata = pmt
        podtemp.spec = podspec

        dcspec.replicas = 1
        dcspec.selector = {"label": idname}
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

    def createroute(self, target, idname, namespace, service, nameapp):
        rbody = openshift.client.V1Route()
        routemeta = V1ObjectMeta()
        routespec = openshift.client.V1RouteSpec()
        routeport = openshift.client.V1RoutePort()
        routeto = openshift.client.V1RouteTargetReference()

        routeport.target_port = target
        routeto.kind = 'Service'
        routeto.name = idname
        routeto.weight = 100

        routespec.host = idname + '.web.rmlab.infn.it'
        routespec.port = routeport
        routespec.to = routeto

        routemeta.labels = {"label": idname, "bundle": service + "-" + nameapp}
        routemeta.name = idname
        routemeta.namespace = namespace

        rbody.api_version = 'v1'
        rbody.kind = 'Route'
        rbody.metadata = routemeta
        rbody.spec = routespec

        try:
            self.o1.create_namespaced_route(namespace=namespace, body=rbody, pretty='true')

        except ApiException as e:
            print("Exception when calling OapiApi->create_route: %s\n" % e)

