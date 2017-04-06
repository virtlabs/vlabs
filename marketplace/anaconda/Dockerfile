FROM continuumio/anaconda3

RUN apt-get update
RUN apt-get install -y gcc python2.7 vim

RUN /opt/conda/bin/conda install jupyter -y --quiet && mkdir /opt/notebooks && mkdir /root/scripts

RUN pip install bash_kernel
RUN python -m bash_kernel.install

ADD ./notebook.sh /root/scripts/notebook.sh
RUN chmod 655  /root/scripts/notebook.sh

ENTRYPOINT  ["/root/scripts/notebook.sh"]
