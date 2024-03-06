#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://www.freedesktop.org/software/fontconfig/release/fontconfig-$VERSION.tar.gz || exit 1
tar -xf "fontconfig-$VERSION.tar.gz" || exit 1
cd "fontconfig-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs
