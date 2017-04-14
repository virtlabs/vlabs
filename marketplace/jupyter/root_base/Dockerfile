FROM virtuallabs/jupyterbase

RUN apt-get update
RUN apt-get install -y build-essential libstdc++-4.8-dev

RUN mkdir /RT && cd /RT &&  wget https://root.cern.ch/download/root_v6.08.06.Linux-ubuntu14-x86_64-gcc4.8.tar.gz && tar -xvf root_v6.08.06.Linux-ubuntu14-x86_64-gcc4.8.tar.gz
RUN pip install metakernel


ADD ./notebook.sh /root/scripts/notebook.sh

RUN chmod 755  /root/scripts/notebook.sh

EXPOSE 8888

ENTRYPOINT  ["/root/scripts/notebook.sh"]
