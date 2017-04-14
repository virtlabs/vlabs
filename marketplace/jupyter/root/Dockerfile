FROM continuumio/anaconda

RUN apt-get update
RUN apt-get install -y vim wget build-essential libstdc++-4.8-dev

RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts
RUN mkdir /RT && cd /RT &&  wget https://root.cern.ch/download/root_v6.08.06.Linux-ubuntu14-x86_64-gcc4.8.tar.gz && tar -xvf root_v6.08.06.Linux-ubuntu14-x86_64-gcc4.8.tar.gz

RUN pip install metakernel
RUN conda install -c conda-forge matplotlib=2.0.0
RUN conda install -c r r

ADD ./notebook.sh /root/scripts/notebook.sh
ADD ./setpasswd.py /root/scripts/setpasswd.py

RUN chmod 755  /root/scripts/notebook.sh
RUN chmod 755  /root/scripts/setpasswd.py

EXPOSE 8888

ENTRYPOINT  ["/root/scripts/notebook.sh"]
