#!/bin/bash

git clone -b "$@" "git://source.winehq.org/git/vkd3d.git" "/root/vkd3d"

cd "/root/vkd3d" || exit 1

### Environment preparation
export PATH="/root/wine-tools/tools/widl/:$PATH"

./autogen.sh || exit 1

./configure --host x86_64-apple-darwin17 --prefix="" || exit 2
make || exit 3
make install DESTDIR="/opt/local/" || exit 4
libtool --finish /opt/local/lib || exit 5

# Copy the VKD3D headers into macports location
cp -r /root/vkd3d/include/* /opt/local/include

exit 0
