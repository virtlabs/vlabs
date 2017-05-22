from __future__ import print_function
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


CONF="/root/.kube/config"

config.load_kube_config()
r1 = openshift.client.OapiApi()
v1 = kubernetes.client.CoreV1Api()
#objects definitions
deploymentconfig = openshift.client.V1DeploymentConfig()
mt = V1ObjectMeta()
pmt = V1ObjectMeta()
rspec = openshift.client.V1DeploymentConfigSpec()
podtemp = client.V1PodTemplateSpec()
podspec = client.V1PodSpec()
container = client.V1Container()
envvar1 = client.V1EnvVar()
envvar2 = client.V1EnvVar()
envvar3 = client.V1EnvVar()
envvar4 = client.V1EnvVar()
envvar5 = client.V1EnvVar()
bservice = client.V1Service()
smeta = V1ObjectMeta()
sspec = client.V1ServiceSpec()
servports = client.V1ServicePort()
containerports = client.V1ContainerPort()
strategy = openshift.client.V1DeploymentStrategy()
rollingparams = openshift.client.V1RollingDeploymentStrategyParams()

#variables
ns='test-project'
av = 'v1'

#v metadata
app = 'app'
namelabel = 'test01'
namerc = 'test01'

#spec replication controller
numrep = 1
deploy = 'deploymentconfig'
slct = {deploy:namelabel}

#podspec
podname='podv1'
imagename = 'virtuallabs/moodlevlabs'
cntname = 'test01-v1'

#servicesvar
nameservice = 'test'
portname = '80-tcp'
prtcl = 'TCP'
prt = 80
tport = '80-tcp'

podlabel = {'name':'podv1'}


servports.name = portname
servports.protocol = prtcl
servports.port = prt
servports.target_port = tport

smeta.name = nameservice
smeta.namespace = ns
smeta.labels = podlabel
sspec.selector = podlabel ###{app:namelabel, nameservice:namelabel}
sspec.ports = [servports]
bservice.api_version = av
bservice.kind = 'Service'
bservice.metadata = smeta
bservice.spec = sspec
print("Starting pods creation:")
containerports.container_port = prt
containerports.name = portname ######################################################################################################


envvar1.name = 'DB_HOST'
envvar1.value = "''"
envvar2.name = 'DB_NAME'
envvar2.value = "''"
envvar3.name = 'DB_USER'
envvar3.value = "''"
envvar4.name = 'DB_PASSWD'
envvar4.value = "''"
envvar5.name = 'WWW_ROOT'
envvar5.value = "''"



container.image = imagename
container.name = cntname
container.env = [envvar1, envvar2, envvar3, envvar4, envvar5]
container.ports = [containerports]
pmt.labels = podlabel ###{app:namelabel, nameservice:namelabel}
pmt.name = podname
podspec.containers = [container]
##############podspec.volumes
podtemp.metadata = pmt
podtemp.spec = podspec
rollingparams.interval_seconds = 1
strategy.labels = podlabel
strategy.type = 'Rolling'
strategy.rolling_params = rollingparams
rspec.replicas = numrep
rspec.selector =  podlabel   #{app:namelabel, nameservice:namelabel}
rspec.template = podtemp
rspec.strategy = strategy
mt.labels = podlabel #{'labelrc':'labelrc'} ###{app:namelabel}
mt.name = namerc
mt.namespace = ns

deploymentconfig.api_version = av
deploymentconfig.metadata = mt
deploymentconfig.spec = rspec
deploymentconfig.kind = 'DeploymentConfig'
 

####creazione rotta



#def objects
rbody = openshift.client.V1Route()
routemeta = V1ObjectMeta()
routespec = openshift.client.V1RouteSpec()
routeport = openshift.client.V1RoutePort()
routeto = openshift.client.V1RouteTargetReference()

#def var
routename = 'moodletest'


routeport.target_port = tport
routeto.kind = 'Service'
routeto.name = nameservice
routeto.weight = 100


routespec.host = ''
routespec.port = routeport
routespec.to = routeto


routemeta.labels = podlabel
routemeta.name = routename
routemeta.namespace = ns



rbody.api_version = av
rbody.kind = 'Route'
rbody.metadata = routemeta
rbody.spec = routespec








################ mysql

mymeta = V1ObjectMeta()
myspec = client.V1ServiceSpec()
myport = client.V1ServicePort()

myport.name = '3306-tcp'
myport.port = 3306
myport.protocol = 'TCP'
myport.target_port = 3306

mymeta.labels = {'label':'mysql'}
mymeta.name = 'db'
mymeta.namespace = ns

myspec.ports = [myport]
myspec.selector = {'label':'mysql'}


mys = client.V1Service()
mys.api_version = av
mys.kind = 'Service'
mys.metadata = mymeta
mys.spec = myspec



dcmysq = openshift.client.V1DeploymentConfig()

dcmysqlstrat = openshift.client.V1DeploymentStrategy()

dcmysqltemp = client.V1PodTemplateSpec()
mysqlcontainer = client.V1Container()

dcmysqlstrat.labels = {'label':'mysql'}
dcmysqlstrat.type = 'Rolling'

mysqlpodmeta = V1ObjectMeta()
mysqlpodspec = V1PodSpec()
mysqlvar1 = client.V1EnvVar()
mysqlvar2 = client.V1EnvVar()
mysqlvar3 = client.V1EnvVar()
mysqlvar4 = client.V1EnvVar()



mysqlvar1.name = 'MYSQL_DATABASE'
mysqlvar1.value = ''
mysqlvar2.name = 'MYSQL_ROOT_PASSWORD'
mysqlvar2.value = ''
mysqlvar3.name = 'MYSQL_USER'
mysqlvar3.value = ''
mysqlvar4.name = 'MYSQL_PASSWORD'
mysqlvar4.value = ''

mysqlports = client.V1ContainerPort()
mysqlports.container_port = 3306
mysqlports.name = '3306-tcp'




mysqlpodspec.containers = [mysqlcontainer]
mysqlcontainer.env = [mysqlvar1, mysqlvar2, mysqlvar3, mysqlvar4]
mysqlcontainer.image = 'mysql:latest'
mysqlcontainer.ports = [mysqlports]
mysqlcontainer.name = 'db'


mysqlpodmeta.labels = {'label':'mysql'}
mysqlpodmeta.name = 'podmysql'
mysqlpodmeta.namespace = ns

dcmysqltemp.metadata = mysqlpodmeta
dcmysqltemp.spec = mysqlpodspec


dcmysqmeta = V1ObjectMeta()
dcmysqmeta.labels = {'label':'mysql'}
dcmysqmeta.name = 'dcmysql'
dcmysqmeta.namespace = ns

dcmysqspec = openshift.client.V1DeploymentConfigSpec()
dcmysqspec.replicas = 1
dcmysqspec.selector = {'label':'mysql'}
dcmysqspec.strategy = dcmysqlstrat
dcmysqspec.template = dcmysqltemp


dcmysq.api_version = av
dcmysq.kind = 'DeploymentConfig'
dcmysq.metadata = dcmysqmeta
dcmysq.spec = dcmysqspec




try:
    v1.create_namespaced_service(namespace=ns, body=bservice, pretty='true')
    r1.create_namespaced_deployment_config(namespace=ns, body=deploymentconfig, pretty='true')

    v1.create_namespaced_service(namespace=ns, body=mys, pretty='true')
    r1.create_namespaced_deployment_config(namespace=ns, body=dcmysq, pretty='true')

    r1.create_namespaced_route(namespace=ns, body=rbody, pretty='true')



except ApiException as e:
    print("Exception when calling OapiApi->create_namespaced_route: %s\n" % e)

