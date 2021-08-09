#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://www.libsdl.org/release/SDL2-$VERSION.tar.gz || exit 1
tar -xvf "SDL2-$VERSION.tar.gz" || exit 1
cd "SDL2-$VERSION" || exit 1

[ "$ARCH" = "x86_64" ] && configure_options="--disable-render-metal"

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install-hdrs DESTDIR="/build/$ARCH/" || exit 2
make install-lib DESTDIR="/build/$ARCH/" || exit 2
make install-data  DESTDIR="/build/$ARCH/" || exit 2

install-libs