#!/bin/bash

. /build-scripts/common.sh

prepare

git clone -b "${VERSION}" https://github.com/FNA-XNA/FAudio || exit 1
cd "FAudio" || exit 1
patch -p0 < /build-scripts/faudio.patch || exit 1

mkdir "/src/$ARCH" || exit 1
cd "/src/$ARCH" || exit 1

$ARCH-apple-darwin17-cmake /src/FAudio || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/" || exit 2
mv /build/"$ARCH"/usr/ /build/"$ARCH"/opt

install-libs

ln -s /opt/local/lib/libFAudio.0.$VERISON.dylib /opt/local/lib/libFAudio.dylib || exit 3
ln -s /opt/local/lib/libFAudio.0.$VERSION.dylib /opt/local/lib/libFAudio.0.dylib || exit 3