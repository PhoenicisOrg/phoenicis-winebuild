#!/bin/bash

if [ "$VERSION" = "" ]; then
  echo "Please specify gnutls version (env VERSION)"
  exit 1
fi

if [ "$ARCH" = "" ]; then
  echo "Please specify architecture (env ARCH)"
  exit 1
fi

[ "$ARCH" = "i386" ] && LIB_DIRECTORY="lib32"
[ "$ARCH" = "x86_64" ] && LIB_DIRECTORY="lib64"


wget https://nlnetlabs.nl/downloads/unbound/unbound-$VERSION.tar.gz || exit 1
tar -xvf "unbound-$VERSION.tar.gz" > /dev/null || exit 1
cd "unbound-$VERSION" || exit 1

rm -r /build
./configure --host "$ARCH"-apple-darwin17 --prefix="/build/$ARCH/" --with-included-unistring || exit 2
make -j 4 || exit 2
make install || exit 2

cd "/build/$ARCH/" || exit 3
cp -r lib/* "/opt/local/$LIB_DIRECTORY" || exit 4
cp -r include/* "/opt/local/include/" || exit 4