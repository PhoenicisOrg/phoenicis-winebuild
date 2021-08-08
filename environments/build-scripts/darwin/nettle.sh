#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://ftp.gnu.org/gnu/nettle/nettle-$VERSION.tar.gz || exit 1
tar -xvf "nettle-$VERSION.tar.gz" || exit 1
cd "nettle-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 --disable-assembler --enable-mini-gmp --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs