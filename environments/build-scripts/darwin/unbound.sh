#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://nlnetlabs.nl/downloads/unbound/unbound-$VERSION.tar.gz || exit 1
tar -xvf "unbound-$VERSION.tar.gz" > /dev/null || exit 1
cd "unbound-$VERSION" || exit 1

./configure --host "$ARCH"-apple-darwin17 --prefix="/build/$ARCH/" --with-included-unistring --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs