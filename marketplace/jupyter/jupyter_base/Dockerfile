FROM continuumio/miniconda

RUN apt-get update

RUN apt-get install -y vim wget 

RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts


ADD ./notebook.sh /root/scripts/notebook.sh
ADD ./setpasswd.py /root/scripts/setpasswd.py


RUN chmod 755  /root/scripts/notebook.sh
RUN chmod 755  /root/scripts/setpasswd.py

EXPOSE 8888

ENTRYPOINT  ["/root/scripts/notebook.sh"]

