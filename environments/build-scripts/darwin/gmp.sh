#!/bin/bash
. /build-scripts/common.sh

prepare

wget https://gmplib.org/download/gmp/gmp-$VERSION.tar.xz || exit 1
tar -xvf "gmp-$VERSION.tar.xz" || exit 1
cd "gmp-$VERSION" || exit 1


./configure --host "$ARCH"-apple-darwin17 --prefix="/build/$ARCH/" || exit 2
make all -j 4 || exit 2
make install -j 4 || exit 2


stage-libs