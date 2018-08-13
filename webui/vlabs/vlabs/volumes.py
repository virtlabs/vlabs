from __future__ import print_function
import time
import kubernetes.client
from kubernetes.client.rest import ApiException
from pprint import pprint
from kubernetes import config, client
from kubernetes.client.models.v1_object_meta import V1ObjectMeta
import openshift.client.models
import kubernetes.client.models
from kubernetes.client.models import V1PersistentVolumeSpec, V1PersistentVolumeStatus, V1ResourceRequirements
import openshift.client
from kubernetes.client.models.v1_glusterfs_volume_source import V1GlusterfsVolumeSource
from kubernetes.client.models.v1_persistent_volume_claim_spec import V1PersistentVolumeClaimSpec
from kubernetes.client.models.v1_label_selector import V1LabelSelector


class Vol:
    def __init__(self, user, selectedproject):
        cfg = '/root/.kube/' + user + '.config'
        self.namespace = selectedproject
        self.apiver = 'v1'
        kcfg = kubernetes.config.new_client_from_config(cfg)
        self.k1 = kubernetes.client.CoreV1Api(kcfg)

    # non usata, si pu(o con l'accento) cancellare
    def createvolume(self, nameapp, deploy, datadir):
        idname = nameapp + "-" + deploy
        
        vbody = kubernetes.client.V1PersistentVolume()
        volmeta = V1ObjectMeta()
        volspec = V1PersistentVolumeSpec()
        gfs = V1GlusterfsVolumeSource()
        accessmode = ['ReadWriteMany']

        ################################################# - V1ObjectMeta()
        volmeta.labels = {'label': idname}
        volmeta.namespace = self.namespace
        volmeta.name = 'pv-' + idname

        ################################################# - gfs
        gfs.endpoints = 'pv-' + idname
        gfs.path = datadir
        gfs.server = nameapp + "-" + deploy

        ################################################# - V1PersistentVolumeSpec()
        volspec.access_modes = accessmode
        volspec.capacity = {'storage': '1Gi'}
        volspec.glusterfs = gfs
        volspec.persistent_volume_reclaim_policy = 'Recycle'
        volspec.storage_class_name = 'glusterfs-storage'

        vbody.api_version = self.apiver
        vbody.kind = 'PersistentVolume'
        vbody.metadata = volmeta
        vbody.spec = volspec

        try:
            api_response = self.k1.create_persistent_volume(vbody, pretty='true')
            pprint(api_response)
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_persistent_volume: %s\n" % e)


    def pvc(self, nameapp, deploy, volspace):
        idname = nameapp + "-" + deploy
        volumename = 'pv-' + idname

        pvcb = kubernetes.client.V1PersistentVolumeClaim()  # V1PersistentVolumeClaim |
        pretty = 'true'
        accessmode = ['ReadWriteMany']

        pvcmeta = V1ObjectMeta()
        pvcspec = V1PersistentVolumeClaimSpec()
        selector = V1LabelSelector()
        requirements = V1ResourceRequirements()

        ##################################################pvcmeta
        pvcmeta.namespace = self.namespace
        pvcmeta.name = volumename
        pvcmeta.labels = {'label': idname}

        ##################################################pvcspec
        selector.match_label = {'label': idname}

        requirements.limits = {'storage': volspace}
        requirements.requests = {'storage': volspace}

        pvcspec.access_modes = accessmode
        #pvcspec.selector = selector
        #pvcspec.volume_name = volumename
        pvcspec.storage_class_name = 'glusterfs-storage'
        pvcspec.resources = requirements

        ##################################################pvcbody
        pvcb.api_version = 'v1'
        pvcb.kind = 'PersistentVolumeClaim'
        pvcb.metadata = pvcmeta
        pvcb.spec = pvcspec

        try:
            api_response = self.k1.create_namespaced_persistent_volume_claim(self.namespace, pvcb, pretty=pretty)
            pprint(api_response)
            return volumename
        except ApiException as e:
            print("Exception when calling CoreV1Api->create_namespaced_persistent_volume_claim: %s\n" % e)
