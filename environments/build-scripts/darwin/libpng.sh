#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://freefr.dl.sourceforge.net/project/libpng/libpng16/$VERSION/libpng-$VERSION.tar.gz || exit 1
tar -xf "libpng-$VERSION.tar.gz" || exit 1
cd "libpng-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs
