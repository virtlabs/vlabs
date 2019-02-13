import kubernetes.config as kconf
import kubernetes.client
from kubernetes.client.rest import ApiException
import openshift.client
import openshift.config as oconf
import logging

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
                         'status': api_response.items[i].status,
                         'dirpvc': api_response.items[i].spec.template.spec.containers[0].volume_mounts
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
            logging.info(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespace: %s\n" % e)

    def readquotas(self, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        timeout_seconds = 56

        try:
            api_response = api_instance.list_namespaced_resource_quota(namespace, timeout_seconds=timeout_seconds)
            logging.info(api_response)
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
            logging.info(api_response)
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
            logging.info(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->patch_namespaced_limit_range: %s\n" % e)

    def readlimit(self, namespace, name):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        try:
            api_response = api_instance.read_namespaced_limit_range(name, namespace)
            logging.info(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_limit_range: %s\n" % e)

    def readsinglequota(self, namespace, name):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)

        try:
            api_response = api_instance.read_namespaced_resource_quota(name, namespace)
            logging.info(api_response)
            return(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->read_namespaced_resource_quota: %s\n" % e)

    def setquotas(self, namespace, body):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        try:
            api_response = api_instance.create_namespaced_resource_quota(namespace, body)
            logging.info(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_resource_quota: %s\n" % e)

    def updatedconfig(self, name, namespace, body):
        api_instance = openshift.client.AppsOpenshiftIoV1Api(self.ocfg)

        try:
            api_response = api_instance.patch_namespaced_deployment_config(name, namespace, body)
            logging.info(api_response)
            return api_response
        except ApiException as e:
            print("Exception when calling AppsOpenshiftIoV1Api->patch_namespaced_deployment_config: %s\n" % e)

    def dellimit(self, name, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        body = kubernetes.client.V1DeleteOptions()

        try:
            api_response = api_instance.delete_namespaced_limit_range(name, namespace, body)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_limit_range: %s\n" % e)

    def delquota(self, name, namespace):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        body = kubernetes.client.V1DeleteOptions()  # V1DeleteOptions |

        try:
            api_response = api_instance.delete_namespaced_resource_quota(name, namespace, body)
            return api_response
        except ApiException as e:
            print("Exception when calling CoreV1Api->delete_namespaced_resource_quota: %s\n" % e)

    def listnodes(self):
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        nodes = {}
        try:
            api_response = api_instance.list_node()
            for i in range(0, len(api_response.items)):
                for k in range(0, len(api_response.items[i].status.conditions)):
                    if api_response.items[i].status.conditions[k].type == 'Ready':
                        nodes[api_response.items[i].metadata.name] = api_response.items[i].status.conditions[k].status
            return nodes
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_node: %s\n" % e)

    def readuser(self, user):
        api_instance = openshift.client.UserOpenshiftIoV1Api(self.ocfg)

        try:
            usr = api_instance.read_user(user, pretty='true', exact='true', export='true')
            return usr
        except ApiException as e:
            print("Exception when calling UserOpenshiftIoV1Api->read_user: %s\n" % e)


    def createuser(self):
        pass

    def deluser(self):
        pass

    def listroleb(self, name, namespace):
        api_instance = openshift.client.AuthorizationOpenshiftIoV1Api(self.ocfg)

        try:
            api_response = api_instance.read_namespaced_role_binding(name, namespace)
            logging.info(api_response)
        except ApiException as e:
            print("Exception when calling AuthorizationOpenshiftIoV1Api->list_namespaced_role_binding: %s\n" % e)


    def replacerolebinding(self, namespace, user, operation):
        api_instance = openshift.client.AuthorizationOpenshiftIoV1Api(self.ocfg)
        name = 'admin'
        body = api_instance.read_namespaced_role_binding(name, namespace)
        if operation == 'add':
            body.user_names.append(user)
        elif operation == 'del':
            body.user_names.remove(user)
        try:
            api_response = api_instance.replace_namespaced_role_binding(name, namespace, body)
            logging.info(api_response)
        except ApiException as e:
            print("Exception when calling AuthorizationOpenshiftIoV1Api->replace_namespaced_role_binding: %s\n" % e)

    def createns(self, newns, username):
        good = False
        api_instance = kubernetes.client.CoreV1Api(self.kcfg)
        body = kubernetes.client.V1Namespace()
        body.kind = 'Namespace'
        body.metadata = kubernetes.client.V1ObjectMeta()
        body.metadata.name = newns
        body.metadata.annotations = {"openshift.io/display-name": newns}
        body.metadata.labels = {'namespace': 'v-labs'}
        try:
            api_response = api_instance.create_namespace(body, pretty='true')
            logging.info(api_response)
            good = True
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespace: %s\n" % e)
        if good:
            api_instance = openshift.client.AuthorizationOpenshiftIoV1Api(self.ocfg)
            body = openshift.client.V1RoleBinding()  # V1alpha1RoleBinding |
            body.kind = 'RoleBinding'
            body.metadata = {'name':"system:deployers"}
            body.role_ref = {'name':"system:deployer"}
            body.subjects = []
            body.subjects.append({})
            body.subjects[0] = {"kind": "ServiceAccount", "name": "deployer", "namespace": newns}
            string = "system:serviceaccount:" + newns + ":deployer"
            body.user_names = []
            body.user_names.append(string)

            bodyb = openshift.client.V1RoleBinding()
            bodyb.kind = 'RoleBinding'
            bodyb.metadata = {'name': "system:image-builders"}
            bodyb.role_ref = {'name': "system:image-builder"}
            bodyb.subjects = []
            bodyb.subjects.append({})
            bodyb.subjects[0] = {"kind": "ServiceAccount", "name": "builder", "namespace": newns}
            string = "system:serviceaccount:" + newns + ":builder"
            bodyb.user_names = []
            bodyb.user_names.append(string)

            bodyc = openshift.client.V1RoleBinding()
            bodyc.kind = 'RoleBinding'
            bodyc.metadata = {'name': "system:image-pullers"}
            bodyc.role_ref = {'name': "system:image-puller"}
            bodyc.subjects = []
            bodyc.subjects.append({})
            string = "system:serviceaccounts:" + newns
            bodyc.subjects[0] = {"kind": "SystemGroup", "name": string}

            adminrole = openshift.client.V1RoleBinding()
            adminrole.kind = 'RoleBinding'
            adminrole.metadata = {'name': "admin"}
            adminrole.role_ref = {'name': "admin"}
            adminrole.subjects = []
            adminrole.subjects.append({'kind': 'User', 'name': username})
            adminrole.user_names = []
            adminrole.user_names.append(username)

            try:
                api_response = api_instance.create_namespaced_role_binding(newns, body)
                logging.info(api_response)
                api_response = api_instance.create_namespaced_role_binding(newns, bodyb)
                logging.info(api_response)
                api_response = api_instance.create_namespaced_role_binding(newns, bodyc)
                logging.info(api_response)
                api_response = api_instance.create_namespaced_role_binding(newns, adminrole)
                logging.info(api_response)

                #create empty user role binding
                #user = openshift.client.V1RoleBinding()
                #user.kind = "RoleBinding"
                #api_response = api_instance.create_namespaced_role_binding(newns, user)
                #print(api_response)
            except ApiException as e:
                print("Exception when calling RbacAuthorizationV1alpha1Api->create_namespaced_role_binding: %s\n" % e)
        return good