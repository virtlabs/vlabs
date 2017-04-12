FROM continuumio/anaconda

RUN apt-get update
RUN apt-get install -y gcc vim libxft2 libxpm4

RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts

RUN pip install bash_kernel
RUN python -m bash_kernel.install

RUN conda config --add channels https://conda.anaconda.org/NLeSC


ADD ./notebook.sh /root/scripts/notebook.sh
RUN chmod 655  /root/scripts/notebook.sh

ENTRYPOINT  ["/root/scripts/notebook.sh"]

