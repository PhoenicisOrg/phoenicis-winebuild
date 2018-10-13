FROM i386/debian:jessie

RUN echo 'deb-src http://deb.debian.org/debian jessie main' >> /etc/apt/sources.list
RUN echo 'deb-src http://security.debian.org/debian-security jessie/updates main' >> /etc/apt/sources.list
RUN echo 'deb-src http://deb.debian.org/debian jessie-updates main' >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y build-dep wine
RUN apt-get -y install git

RUN cd /root
