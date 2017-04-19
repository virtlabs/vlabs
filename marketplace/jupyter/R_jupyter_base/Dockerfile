FROM virtuallabs/jupyterbase3

RUN apt-get update && apt-get install -y libcurl4-openssl-dev build-essential

RUN apt-get -y install libcurl4-gnutls-dev
RUN conda install r-base

RUN conda install -c r r-irkernel=0.7.1

ENTRYPOINT  ["/root/scripts/notebook.sh"]