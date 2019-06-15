FROM i386/debian:stretch

RUN echo 'deb-src http://deb.debian.org/debian stretch main' >> /etc/apt/sources.list
RUN echo 'deb-src http://security.debian.org/debian-security stretch/updates main' >> /etc/apt/sources.list
RUN echo 'deb-src http://deb.debian.org/debian stretch-updates main' >> /etc/apt/sources.list

RUN apt-get update
RUN apt-get -y build-dep wine
RUN apt-get -y install libkrb5-dev opencl-dev libpcap-dev libsane-dev libv4l-dev libgphoto2-dev libtiff-dev libpulse-dev libgstreamer1.0-dev libudev-dev libcapi20-dev libgstreamer-plugins-base1.0-dev
RUN apt-get -y install git libdbus-1-dev fcitx-libs-dev libsamplerate0-dev libibus-1.0-dev
RUN apt-get -y install mingw-w64

# Wine Staging
RUN apt-get -y install gtk3.0-dev libgtk-3-dev libva-dev
RUN apt-get -y install libavcodec-dev

# Vulkan
RUN apt-get -y install libvulkan-dev

# VKD3D
RUN apt-get -y install wget
RUN mkdir -p /root/vkd3d
WORKDIR /root/vkd3d
RUN wget http://cdn-fastly.deb.debian.org/debian/pool/main/v/vulkan/libvulkan1_1.1.70+dfsg1-1~bpo9+1_i386.deb
RUN wget http://deb.debian.org/debian/pool/main/v/vkd3d/libvkd3d-dev_1.1-3_i386.deb
RUN wget http://deb.debian.org/debian/pool/main/v/vkd3d/libvkd3d1_1.1-3_i386.deb
RUN wget http://ftp.de.debian.org/debian/pool/main/v/vkd3d/libvkd3d-utils1_1.1-3_i386.deb
RUN wget http://cdn-fastly.deb.debian.org/debian/pool/main/v/vulkan/libvulkan-dev_1.1.70+dfsg1-1~bpo9+1_i386.deb
RUN dpkg -i *.deb

#OSSv4
RUN mkdir -p /root/ossv4
WORKDIR /root/ossv4
RUN wget http://deb.debian.org/debian/pool/main/o/oss4/oss4-dev_4.2-build2010-2_all.deb
RUN dpkg -i *.deb

#SDL (for FAudio)
RUN mkdir -p /root/sdl2
WORKDIR /root/sdl2
RUN wget https://www.libsdl.org/release/SDL2-2.0.9.tar.gz
RUN tar -xvf SDL2-2.0.9.tar.gz
WORKDIR /root/sdl2/SDL2-2.0.9/
RUN ./configure --prefix="/usr/"
RUN make
RUN make install

#Faudio
RUN apt-get update
RUN apt-get -y install cmake
RUN mkdir -p /root/faudio
WORKDIR /root/faudio
RUN git clone https://github.com/FNA-XNA/FAudio
RUN mkdir -p /root/faudio/build
WORKDIR /root/faudio/build
RUN cmake /root/faudio/FAudio
RUN make
RUN make install
