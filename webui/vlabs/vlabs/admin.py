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

###controlla field selector e label selector
class Adminclass:
    def __init__(self, admin):
        config_file = '/root/.kube/' + admin + '.config'
        self.kcfg = kconf.new_client_from_config(config_file)
        self.ocfg = oconf.new_client_from_config(config_file)

    def readnsdc(self, namespace):
        api_instance = openshift.client.AppsOpenshiftIoV1Api(self.ocfg)
        try:
            api_response = api_instance.list_namespaced_deployment_config(namespace)
            svcinfos = []
            for i in range(0, len(api_response.items)):
                if 'bundle' in api_response.items[i].metadata.labels.keys():
                    svcinfos.append(
                        {'name': api_response.items[i].metadata.name,
                         'replicas': api_response.items[i].spec.replicas,
                         'status': api_response.items[i].status
                         })
                else:
                    pass
            return(svcinfos)
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_replication_controller: %s\n" % e)

    def delns(self, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions | controlla
        grace_period_seconds = 56
        propagation_policy = 'Background'

        try:
            api_response = api_instance.delete_namespace(namespace, body, grace_period_seconds=grace_period_seconds,
                                                         propagation_policy=propagation_policy)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespace: %s\n" % e)

    def readquotas(self, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56

        try:
            api_response = api_instance.list_namespaced_resource_quota(namespace, timeout_seconds=timeout_seconds)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_resource_quota: %s\n" % e)

    def readallquotas(self):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56
        label_selector = "label=vlabs"
        newarray = []

        try:
            api_response = api_instance.list_resource_quota_for_all_namespaces(timeout_seconds=timeout_seconds)
            if api_response.items:
                newarray.append(api_response.items[0])
                for i in range(0, len(api_response.items)):
                    set = False
                    for k in range(0, len(newarray)):
                        if api_response.items[i].metadata.name == newarray[k].metadata.name:
                            set = True
                    if set==False:
                        newarray.append(api_response.items[i])
            else:
                pass
            return newarray
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_resource_quota_for_all_namespaces: %s\n" % e)

    def readlimits(self, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56
        try:
            api_response = api_instance.list_namespaced_limit_range(namespace, timeout_seconds=timeout_seconds)
            print(api_response)
            return api_response.items
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_namespaced_limit_range: %s\n" % e)

    def readalllimits(self):
        api_instance = kubernetes.client.CoreV1Api(self.ocfg)
        label_selector = "label=vlabs"
        timeout_seconds = 56  # int | Timeout for the list/watch call. (optional)
        newarray = []
        try:
            api_response = api_instance.list_limit_range_for_all_namespaces(timeout_seconds=timeout_seconds)
            if api_response.items:
                newarray.append(api_response.items[0])
                for i in range(1, len(api_response.items)):
                    set = False
                    for k in range(0, len(newarray)):
                        if api_response.items[i].metadata.name == newarray[k].metadata.name and api_response.items[i].spec == newarray[k].spec:
                            set=True
                    if set == False:
                        newarray.append(api_response.items[i])
            else:
                pass
            return newarray
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_limit_range_for_all_namespaces: %s\n" % e)

    def setlimits(self, namespace, body):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        #body = kubernetes.client.V1LimitRange()

        try:
            api_response = api_instance.create_namespaced_limit_range(namespace, body)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_limit_range: %s\n" % e)

    def patchlimits(self, namespace, name, body):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)

        try:
            api_response = api_instance.patch_namespaced_limit_range(name, namespace, body)
            print(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_limit_range: %s\n" % e)

    def readlimit(self, namespace, name):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        try:
            api_response = api_instance.read_namespaced_limit_range(name, namespace)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_limit_range: %s\n" % e)

    def readsinglequota(self, namespace, name):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)

        try:
            api_response = api_instance.read_namespaced_resource_quota(name, namespace)
            print(api_response)
            return(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_resource_quota: %s\n" % e)

    def setquotas(self, namespace, body):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        try:
            api_response = api_instance.create_namespaced_resource_quota(namespace, body)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_resource_quota: %s\n" % e)

    def updatedconfig(self, name, namespace, body):
        api_instance = openshift.client.AppsOpenshiftIoV1Api(self.ocfg)

        try:
            api_response = api_instance.patch_namespaced_deployment_config(name, namespace, body)
            print(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling AppsOpenshiftIoV1Api->patch_namespaced_deployment_config: %s\n" % e)

    def readuser(self):
        pass

    def createuser(self):
        pass

    def deluser(self):
        pass
