from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import config, client
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
import openshift.client.models
import kubernetes.client.models
from kubernetes.client.models import V1PersistentVolumeSpec, V1PersistentVolumeStatus
import openshift.client
from kubernetes.client.models.v1_nfs_volume_source import V1NFSVolumeSource
from kubernetes.client.models.v1_persistent_volume_claim_spec import V1PersistentVolumeClaimSpec
from kubernetes.client.models.v1_label_selector import V1LabelSelector




class Vol:
    def __init__(self, nameapp, deploy, label):
        self.namespace = 'test-project'
        self.apiver = 'v1'
        config.load_kube_config()
        self.k1 = kubernetes.client.CoreV1Api()
        self.idname = nameapp + "-" + deploy
        self.label = label

    def createvolume(self):
        vbody = kubernetes.client.V1PersistentVolume()  # V1PersistentVolume |
        volmeta = V1ObjectMeta()                # to fill
        volspec = V1PersistentVolumeSpec()      # to fill
        nfsvol = V1NFSVolumeSource()
        accessmode = ['ReadWriteMany']

################################################# - V1ObjectMeta()
        volmeta.labels = self.label
        volmeta.namespace = self.namespace
        volmeta.name = self.idname

################################################# - V1NFSVolumeSource() - TO CHANGE!!!!!!!!!!!
        nfsvol.path = '/DATA'
        nfsvol.server = '127.0.0.1'

################################################# - V1PersistentVolumeSpec()
        volspec.access_modes = accessmode
        volspec.capacity = {'1', 'GB'}
#       volspec.mount_options = []
        volspec.nfs = nfsvol
        volspec.persistent_volume_reclaim_policy = 'Recycle'


        vbody.api_version = self.apiver
        vbody.kind = 'PersistentVolume'
        vbody.metadata = volmeta #######to fill
        vbody.spec = volspec

        try:
            api_response = self.k1.create_persistent_volume(vbody, pretty='true')
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_persistent_volume: %s\n" % e)

    def pvc(self):
        pvcb = kubernetes.client.V1PersistentVolumeClaim()  # V1PersistentVolumeClaim |
        pretty = 'true'
        accessmode = ['ReadWriteMany']

        pvcmeta = V1ObjectMeta()
        pvcspec = V1PersistentVolumeClaimSpec()
        selector = V1LabelSelector()

##################################################pvcmeta
        pvcmeta.namespace = self.namespace
        pvcmeta.name = self.idname
        pvcmeta.labels = self.label


##################################################pvcspec
        selector.match_label = self.idname

        pvcspec.access_modes = accessmode
        pvcspec.selector = selector
        pvcspec.volume_name = self.idname


##################################################pvcbody
        pvcb.api_version = 'v1'
        pvcb.kind = 'PersistentVolumeClaim'
        pvcb.metadata = pvcmeta
        pvcb.spec = pvcspec

        try:
            api_response = self.k1.create_namespaced_persistent_volume_claim(self.namespace, pvcb, pretty=pretty)
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e)
