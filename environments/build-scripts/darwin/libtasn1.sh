#!/bin/bash

. /build-scripts/common.sh

prepare

wget http://ftp.gnu.org/gnu/libtasn1/libtasn1-$VERSION.tar.gz || exit 1
tar -xvf "libtasn1-$VERSION.tar.gz" || exit 1
cd "libtasn1-$VERSION" || exit 1
patch -p1 < /build-scripts/libtasn1.patch || exit 1

./configure --host "$ARCH"-apple-darwin17 --prefix="/opt/local" || exit 2
make all -j 4 || exit 2
make install DESTDIR="/build/$ARCH/" || exit 2

install-libs