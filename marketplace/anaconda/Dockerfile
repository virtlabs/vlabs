FROM continuumio/anaconda3


RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts

ADD ./notebook.sh /root/scripts/notebook.sh
RUN chmod 655  /root/scripts/notebook.sh

ENTRYPOINT  ["/root/scripts/notebook.sh"]
