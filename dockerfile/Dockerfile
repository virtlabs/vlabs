FROM python:2.7-stretch

RUN apt-get update && apt-get install -y cron vim supervisor

RUN pip install django=='1.11' django-bootstrap django-bootstrap-themes django-bootstrap3 django-bootstrap4 django-static-jquery PyYAML kubernetes=='3.0.0' openshift=='0.3.4' WhiteNoise

RUN mkdir /vlabs && cd /vlabs && git clone https://github.com/virtlabs/vlabs-source.git

RUN mkdir /openshift && cd /openshift && wget https://github.com/openshift/origin/releases/download/v3.11.0/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz \
 && tar -xvf openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit.tar.gz && mv /openshift/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/oc /usr/local/bin/ && \
 mv  /openshift/openshift-origin-client-tools-v3.11.0-0cbc58b-linux-64bit/kubectl /usr/local/bin/ && rm -rf /openshift

RUN crontab -l ; echo "0 */12 * * * find /root/.kube/* -type f -mmin +360 -delete; find /tmp/* -type f -mmin +360 -delete" | crontab

COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV OKDHOST="example.openshift.domain.com:port"
ENV SVCSDOMAIN=".wildcarddomain.com"
ENV VLROUTE="vlabs.domain"
EXPOSE 8000

CMD supervisord -n

