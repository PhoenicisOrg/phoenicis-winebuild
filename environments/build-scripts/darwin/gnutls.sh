#!/bin/bash
. /build-scripts/common.sh

prepare

wget https://www.gnupg.org/ftp/gcrypt/gnutls/v$MAJOR_VERSION/gnutls-$VERSION.tar.xz || exit 1
tar -xvf "gnutls-$VERSION.tar.xz" > /dev/null || exit 1
cd "gnutls-$VERSION" || exit 1

export NETTLE_CFLAGS="-I/opt/local/include"
export NETTLE_LIBS="-lnettle"

export HOGWEED_CFLAGS="-I/opt/local/include"
export HOGWEED_LIBS="-lhogweed"

export LIBTASN1_CFLAGS="-I/opt/local/include"
export LIBTASN1_LIBS="-ltasn1"

export ac_cv_func_malloc_0_nonnull="yes"
export ac_cv_func_realloc_0_nonnull="yes"
./configure --host "$ARCH"-apple-darwin17 --prefix="/opt/local" --with-included-unistring --without-p11-kit  || exit 2

make clean -j 4 || exit 2
make -j 4 || exit 2
make install DESTDIR="/build/$ARCH/" || exit 2

install-libs