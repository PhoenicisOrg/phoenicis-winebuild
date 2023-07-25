#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://download.savannah.gnu.org/releases/freetype/freetype-$VERSION.tar.xz || exit 1
tar -xf "freetype-$VERSION.tar.xz" || exit 1
cd "freetype-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs
