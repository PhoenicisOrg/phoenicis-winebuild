#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://sourceforge.net/projects/mpg123/files/mpg123/$VERSION/mpg123-$VERSION.tar.bz2 || exit 1
tar -xf "mpg123-$VERSION.tar.bz2" || exit 1
cd "mpg123-$VERSION" || exit 1

[ "$ARCH" = "i386" ] && configure_options="--with-cpu=sse"
[ "$ARCH" = "x86_64" ] && configure_options="--with-cpu=x86-64"

./configure --host $ARCH-apple-darwin17 $configure_options --prefix="/opt/local" || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs
