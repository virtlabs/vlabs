from __future__ import print_function
import time
import openshift.client
from kubernetes.client.rest import ApiException
from kubernetes import config, client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes.client.models.v1_container import V1Container
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
from kubernetes.client.models.v1_pod_spec import V1PodSpec


CONF="/root/.kube/config"
try:
    config.load_kube_config()
    v1=client.CoreV1Api()
    print("Starting pod creation:")
    pod = client.V1Pod()
    pod.metadata = client.V1ObjectMeta(name="prova")
    
    container = client.V1Container()
    container.image = "virtuallabs/prova"
    container.name = "prova-v1"
     
    spec = client.V1PodSpec()
    spec.containers = [container]
    pod.spec = spec

    v1.create_namespaced_pod(namespace='s-prj', body=pod, pretty='true')
    

except ApiException as e:
    print("Exception: %s\n" % e)


