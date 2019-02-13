# V-Labs

V-Labs is a virtual environments provisioning platform binded to Openshift Origin. It permits to instantiate services through a web interface making them reachable by users using only an internet browser and an internet connection.
Once a teacher or an admin is authenticated in his project area in V-Labs he can choose a service from the marketplace and set variables and persistent volumes. A URL address will be returned pointing to the chosen service, making it accessible for his students or researchers.
The yaml defined marketplace describes the available services, every service can be composed by several container images built ad hoc by users or built and released by the Docker Hub community. From the admin-page the administrator can configure the marketplace, combine apps and services and set quotas.
The actual marketplace comprehends learning management systems, Root and Geant4 VMs, CAD, videoconference services, statistical computing and programming languages environments, real-time collaboration and file storage and synchronization services, it can be also expanded with any container image built ad hoc by users or built and released by the Docker Hub community.
V-Labs is written in Python and Django, binded to an existing installation of Openshift Origin with GlusterFS and the Heketi module, independent from the underlying infrastructure, it manages replicas and scalability of pods, replicated persistent volumes mounting and it will be released stand alone and as a docker container.

### N.B.: V-Labs manages only autocreated "v-labs" tagged projects and services. So if you install it on a preexistent OKD instance, you'll not be able to manage your existing projects. This is a feature, in this way V-Labs is harmless to your environment.
### N.BB: Services routes are created by default using a wildcard domain (env SVCSDOMAIN). If you want to certify them you must use a wildcard certificate.

## Features
### No Limitations
- Opensource,
- Binded to an Openshift Origin installation with GlusterFS and Heketi,
- Independent from the underlying structure,
- Marketplace embedded: expandible with any private or public containerized service hosted by the Docker Hub Community,
- Every service is scalable, replicated and monitored,
- Quotas and persistent volumes for any service,
- One or more project areas for every admin.

### No sensible data
- No database: Authn and Authz are managed by Openshift Origin,
- Simple Auth or Identity Providers (LDAP, SAML and others).


## Tecnologies
Python,
Django,
Openshift Origin with GlusterFS and Heketi,
interface: sb-admin2,
Docker.

### Docker Installation
A V-labs Docker container is available on docker hub [virtuallabs/vlabscontainer](https://hub.docker.com/r/virtuallabs/vlabscontainer)

### Dockerfile
If you want to build it by yourself use the dockerfile available in the repository.
It uses PORT 8000 TCP.

### Environment Variables
```
OKDHOST = Openshift web address:port ex. ["openshift.myorg.com:8443"]
SVCSDOMAIN = Wildcard domain of your services ex. [".wildcar.myorg.com"]
VLROUTE = V-Labs web address, default "localhost"
```
```
Optional Variables
DJANGO_SECRET_KEY = A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
DJANGO_DEBUG = Default False. Set to True to enable django debug mode.
CSRF_COOKIE_SECURE = Default False. Whether to use a secure cookie for the CSRF cookie. If this is set to True, the cookie will be marked as “secure,” which means browsers may ensure that the cookie is only sent with an HTTPS connection.
SESSION_COOKIE_SECURE = Default False. Whether to use a secure cookie for the session cookie. If this is set to True, the cookie will be marked as “secure,” which means browsers may ensure that the cookie is only sent under an HTTPS connection.
SECURE_PROXY_SSL_H = Default False.  If True it tells Django to trust the X-Forwarded-Proto header that comes from our proxy, and any time its value is 'https', then the request is guaranteed to be secure (i.e., it originally came in via HTTPS). Equivalent of [SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') ]
PYTHONWARNINGS = Default False. If you want ignore Unverified HTTPS request set to "ignore:Unverified HTTPS request"
```

### Installation from Scratch

Required Packages:
```
cron
supervisor
Openshift CLI [oc command must be in PATH]
python 2.7
pip
```

Required Pip Packages
```
django=='1.11'
django-bootstrap
django-bootstrap-themes
django-bootstrap3
django-bootstrap4
django-static-jquery
PyYAML
kubernetes=='3.0.0'
openshift=='0.3.4'
WhiteNoise
```


## The Marketplace

Tweak the marketplace
If you want to add services to your marketplace you can modify directly ./marketplace/vlabs_template.yml or add others yaml file in the folder ./marketplace/custom_marketplace/
You can also specify the v-labs environment variables OKDHOST and SVCSDOMAIN directly in the principal yaml file.

The yaml defined marketplace defines services and apps. Every app consists in one or more services.

Example, fields description in brackets []:
```
apps:
      - name: 'moodle'			                                            [NAME OF THE APP]
        services:
          - nameservice: 'moodle'	                                 [NAME OF THE FIRST SERVICE]
            ports:
              - port: 'moodle'		                                    [PORT NAME]
                tcp: 80 			                                          [PORT NUMBER]
                route: 'yes' 			                                     [IF PORT CAN BE EXTERNAL ROUTED]
            imagename: 'virtuallabs/moodlevlabs:1.34-1112018-2'   [DOCKER HUB IMAGE NAME]
            env:                                                  [VARIABLES ARRAY - SEE DEDICATED PARAGRAPH]
              - name: 'DB_HOST'
                ….
            volumes:
                persistentvolumeclaim: 'yes'                      [IF A PV CAN BE MOUNTED]
                datadir: '/var/www/moodledata'                    [PV MOUNT PATH]

          - nameservice: 'mysql' 		                                 [SECOND SERVICE]
            ports:
	[...]
```

## Variables Array

Every array element of the variables array is a dictionary of at least 2 key/value pairs: name:val, value:val, description:val (optional).
name: it's the variable name within the container
description: it's the resulting description in v-labs web page
value: it's the variable type and value, it can be:
```

$input: if the value has to be specified V-Labs web page
$random: if the value has to be a random string
$service[service name]: if the value is the name of a service in the same app
$variable[service name:name of the variable]: if the value must be the same of another service environment variable in the same app
$route[service name:port name]: if the value is the route to a specific port of a service (in the same app)
```


## Volumes
V-Labs does not require a persistent volume, however if you want to use a persistent marketplace you can mount your volume in /v-labs/vlabs-source/marketplace/custom_marketplace or if you're using it through OKD you can import your yaml files as Config Maps.


## Use
Docker version
Set up evironment variables and run the CMD
Plain version
```

(to periodically clean the sessions)
crontab -l ; echo "0 */12 * * * find /root/.kube/* -type f -mmin +360 -delete; find /tmp/* -type f -mmin +360 -delete" | crontab
and start cron service
(to start django web-server)
python /vlabs/vlabs-source/manage.py runserver 0:8000 [address:port]
```

A cluster-admin has to login into the v-labs page, he can choose a v-labs project to create/erase/modify a project or go to the admin page. In the admin page he can set up roles for authenticated user authorizing/deauthorizing them to a specified project, he can manage preexisting limits and quotas assigning them to a project and he can take a look on the global situation.

Once a new user is authenticated has no projects assigned, the cluster-admin has to create him a project authorizing him to manage it.

### But Why?
This is a Consortium GARR "Orio Carlini" scholarship project on the application of innovative technologies for the development of digital infrastructures and their services in multidisciplinary contexts.
