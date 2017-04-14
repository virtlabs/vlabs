FROM continuumio/miniconda

RUN apt-get update

RUN apt-get install -y vim wget build-essential libstdc++-4.8-dev

RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts
RUN mkdir /RT 

RUN wget https://root.cern.ch/download/cling/cling_2017-04-12_ubuntu14.tar.bz2 -O /RT/cling_2017-04-12_ubuntu14.tar.bz2 && tar -jxvf /RT/cling_2017-04-12_ubuntu14.tar.bz2 

RUN cd /cling_2017-04-12_ubuntu14/share/cling/Jupyter/kernel && pip install -e . && jupyter-kernelspec install --user cling-cpp17
RUN rm -rf /RT

ADD ./notebook.sh /root/scripts/notebook.sh
ADD ./setpasswd.py /root/scripts/setpasswd.py


RUN chmod 755  /root/scripts/notebook.sh
RUN chmod 755  /root/scripts/setpasswd.py

EXPOSE 8888

ENTRYPOINT  ["/root/scripts/notebook.sh"]

