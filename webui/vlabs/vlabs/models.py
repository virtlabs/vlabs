import json
from django.utils.html import escape, html_safe
from json import dumps
import ast

class ServiceView:
    def __init__(self):
        pass

    def dchart(self, dictbundle):
        jscript = []
        totaljs = []
        knum = 0
        for k in dictbundle:
            chart = {}
            chart['element'] = 'morris-donut-chart' + str(knum)
            chart['resize'] = 'true'
            chart['data'] = []
            chart['colors'] = []
            svcnum = 0
            for kk in dictbundle[k].keys():
                status = dictbundle[k][kk]['status']
                chart['data'].append({})
                chart['data'][svcnum]['label'] = kk
                chart['data'][svcnum]['value'] = 1
                if status == 'True':
                    chart['colors'].append('#00ff00')
                else:
                    chart['colors'].append('#ff0000')
                svcnum = svcnum + 1
            jscript.append(chart)
            knum = knum + 1
        return jscript


    def adminbarchart(self, dictprj):
        arprj = []
        i = 0
        for k in dictprj:
            arprj.append({'y':k, 'a':len(dictprj[k])})
        return arprj

    def userschart(self, usersdict):
        formatlist = []
        for i in range(0, len(usersdict.items)):
            formatlist.append({
                'full_name': usersdict.items[i].full_name,
                'name': usersdict.items[i].metadata.name,
                'identity': usersdict.items[i].identities
            })
        return formatlist

    def usersperns(self, nsdescriptor):
        usersarray = []
        for i in range(0, len(nsdescriptor.items)):
            for j in range(0, len(nsdescriptor.items[i].subjects)):
                if nsdescriptor.items[i].subjects[j].kind == 'User':
                    usersarray.append(nsdescriptor.items[i].subjects[j].name)
                else:
                    pass
        return usersarray

    def pvpvcs(self, dictpv):
        pvd = []
        for i in range(0, len(dictpv.items)):
            pvdict = {}
            pvdict['Name'] = dictpv.items[i].metadata.name
            pvdict['PersistentVolume'] = dictpv.items[i].spec.volume_name
            pvdict['Storage'] = dictpv.items[i].spec.resources.requests['storage']
            pvd.append(pvdict)
        return pvd

    def limitsformat(self, l):
        finallist = []
        for i in range(0, len(l)):
            tempdict = {}
            tempdict['name'] = l[i].metadata.name
            tempdict['spec'] = {}
            for j in range(0, len(l[i].spec.limits)):
                tempdict['spec'][l[i].spec.limits[j].type] = l[i].spec.limits[j]
            finallist.append(tempdict)
        print("\n\n\n\n\n\n\nFINALLIST\n\n\n\n\n\n")
        print(finallist)
        return finallist


class UpdateServices:
    def __init__(self):
            pass

    def varupdate(self, upddict):
        spec = {"spec": {"template": {"spec": {"containers": [{}]}}}}
        spec['spec']['template']['spec']['containers'][0]['name'] = upddict['service']
        del upddict['service']
        spec['spec']['template']['spec']['containers'][0]['env'] = []
        for k in upddict:
            spec['spec']['template']['spec']['containers'][0]['env'].append({'name': k, 'value': upddict[k]})
        print(spec)
        return spec

    def quotaupdate(self, spec_hard=None):
        #{'pods', 'requests.cpu', 'requests.memory', 'requests.ephemeral-storage', 'requests.storage', 'limits.cpu',
        #     'limits.memory', 'limits.memory', 'limits.ephemeral-storage', 'configmaps', 'persistentvolumeclaims',
        #     'replicationcontrollers', 'secrets', 'services'}
        a = {'pods': None, 'requests.cpu': None, 'requests.memory': None, 'requests.ephemeral-storage': None, 'requests.storage': None, 'limits.cpu': None,
             'limits.memory': None, 'limits.memory': None, 'limits.ephemeral-storage': None, 'configmaps': None, 'persistentvolumeclaims': None,
             'replicationcontrollers': None, 'secrets': None, 'services': None}
        if spec_hard:
            for k in spec_hard:
                a[k] = spec_hard[k]
        print(a)
        return a


