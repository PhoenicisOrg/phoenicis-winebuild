#!/bin/bash

. /build-scripts/common.sh

prepare

<<<<<<< HEAD
wget https://download.savannah.gnu.org/releases/freetype/freetype-$VERSION.tar.xz || exit 1
=======
wget https://download.savannah.gnu.org/releases/freetype/freetype-$VERSION.tar.xz || exit 1
>>>>>>> 3b409a4892875922bc993ca8d2f9cf9d13bbc649
tar -xf "freetype-$VERSION.tar.xz" || exit 1
cd "freetype-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs
