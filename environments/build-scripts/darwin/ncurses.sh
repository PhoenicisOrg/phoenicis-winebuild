#!/bin/bash

. /build-scripts/common.sh

prepare

wget https://ftp.gnu.org/pub/gnu/ncurses/ncurses-$VERSION.tar.gz || exit 1
tar -xvf "ncurses-$VERSION.tar.gz" || exit 1
cd "ncurses-$VERSION" || exit 1
patch -p1 < /build-scripts/ncurses.patch || exit 1

export STRIP="$ARCH-apple-darwin17-strip"
export PKG_CONFIG_LIBDIR=/usr/lib/pkgconfig
./configure --host $ARCH-apple-darwin17 --with-shared --with-cxx-shared --enable-widec --disable-lib-suffixes --enable-overwrite --without-debug --without-ada  --with-manpage-format=normal --enable-pc-files --disable-mixed-case  --prefix="/opt/local" --enable-rpath --datarootdir=/usr/share || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/"  || exit 2

install-libs