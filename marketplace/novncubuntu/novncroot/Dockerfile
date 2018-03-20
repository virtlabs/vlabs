FROM virtuallabs/novncubuntu:01032018

#INSTALL ROOT && C++ && gedit && kate

RUN apt-get -y install xfce4-terminal kate gedit build-essential libtbb-dev gfortran libssl-dev libpcre3-dev \
xlibmesa-glu-dev libglew1.5-dev libftgl-dev \
libmysqlclient-dev libfftw3-dev libcfitsio-dev \
graphviz-dev libavahi-compat-libdnssd-dev \
libldap2-dev python-dev libxml2-dev libkrb5-dev \
libgsl0-dev libqt4-dev dpkg-dev cmake g++ gcc binutils libx11-dev libxpm-dev \
libxft-dev libxext-dev && apt autoremove -y

RUN wget https://root.cern.ch/download/root_v6.12.06.Linux-ubuntu16-x86_64-gcc5.4.tar.gz  -P  /myroot && tar xvf /myroot/root_v6.12.06.Linux-ubuntu16-x86_64-gcc5.4.tar.gz && rm -rf /myroot

RUN /bin/bash -c "echo 'source /headless/root/bin/thisroot.sh' >> .bashrc"
