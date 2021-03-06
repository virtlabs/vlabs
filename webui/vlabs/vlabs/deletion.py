import openshift.client.models
import kubernetes.client.models
import openshift.client
from kubernetes.client.rest import ApiException
import logging


class Del():
    def _init_(self):
        pass

    def delsvc(self, svcs, namespace, kcfg):
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        for i in range(0, len(svcs)):
            try:
                api_response = api_instance.delete_namespaced_service(svcs[i], namespace, pretty='true')
                logging.info(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_service: %s\n" % e)

    def deldc(self, dcs, namespace, ocfg):
        api_instance = openshift.client.OapiApi(ocfg)
        body = kubernetes.client.models.V1DeleteOptions()
        body.api_version = 'v1'
        body.kind = 'DeleteOptions'

        for i in range(0, len(dcs)):
            try:
                api_response = api_instance.delete_namespaced_deployment_config(dcs[i], namespace, body, pretty='true',
                                                                                grace_period_seconds=2,
                                                                                orphan_dependents='true')
                logging.info(api_response)
            except ApiException as e:
                print("Exception when calling OapiApi->delete_namespaced_deployment_config: %s\n" % e)

    def delrc(self, rcs, namespace, kcfg):
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        body = kubernetes.client.V1DeleteOptions()
        for i in range(len(rcs)):

            try:
                api_response = api_instance.delete_namespaced_replication_controller(rcs[i], namespace, body,
                                                                                     pretty='true',
                                                                                     grace_period_seconds=2)
                logging.info(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->delete_namespaced_replication_controller: %s\n" % e)

    def delrt(self, rts, namespace, ocfg):
        api_instance = openshift.client.OapiApi(ocfg)
        body = kubernetes.client.models.V1DeleteOptions()
        body.api_version = 'v1'
        body.kind = 'DeleteOptions'
        body.grace_period_seconds = 2

        for i in range(0, len(rts)):
            try:
                api_response = api_instance.delete_namespaced_route(rts[i], namespace, body, pretty='true',
                                                                    orphan_dependents='true')
                logging.info(api_response)
            except ApiException as e:
                print("Exception when calling OapiApi->delete_namespaced_route: %s\n" % e)

    def setrc(self, rcs, namespace, kcfg):
        api_instance = kubernetes.client.CoreV1Api(kcfg)
        body = {'spec': {"replicas": 0}}
        for i in range(len(rcs)):
            try:
                api_response = api_instance.patch_namespaced_replication_controller(rcs[i], namespace, body, pretty='true')
                logging.info(api_response)
            except ApiException as e:
                print("Exception when calling CoreV1Api->patch_namespaced_replication_controller: %s\n" % e)
