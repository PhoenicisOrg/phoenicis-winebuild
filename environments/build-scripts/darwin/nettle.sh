#!/bin/bash

if [ "$VERSION" = "" ]; then
  echo "Please specify nettle version (env VERSION)"
  exit 1
fi

if [ "$ARCH" = "" ]; then
  echo "Please specify architecture (env ARCH)"
  exit 1
fi

[ "$ARCH" = "i386" ] && LIB_DIRECTORY="lib32"
[ "$ARCH" = "x86_64" ] && LIB_DIRECTORY="lib64"

rm -r /build/
export CC="$ARCH-apple-darwin17-clang"
export CXX="$ARCH-apple-darwin17-clang"

wget https://ftp.gnu.org/gnu/nettle/nettle-$VERSION.tar.gz || exit 1
tar -xvf "nettle-$VERSION.tar.gz" || exit 1
cd "nettle-$VERSION" || exit 1

./configure --host $ARCH-apple-darwin17 --prefix="/build/$ARCH/" --disable-assembler --enable-mini-gmp || exit 2
make clean -j 4
make -j 4 || exit 2
make install -j 4 || exit 2

cd "/build/$ARCH/" || exit 3
cp -r lib/* "/opt/local/$LIB_DIRECTORY" || exit 4
cp -r include/* "/opt/local/include/" || exit 4