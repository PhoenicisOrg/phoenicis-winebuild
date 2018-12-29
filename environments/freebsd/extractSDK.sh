mkdir -p /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/include
mkdir -p /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib

tar -xf freebsd$VERSION.sdk.tar.xz
cp -r freebsd$VERSION.sdk/usr/lib/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib
cp -r freebsd$VERSION.sdk/usr/include/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/include
cp -r freebsd$VERSION.sdk/lib/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib
./symlink.sh

mkdir -p /usr/cross-freebsd-32/i386-pc-freebsd$VERSION/include
mkdir -p /usr/cross-freebsd-32/i386-pc-freebsd$VERSION/lib

tar -xf freebsd$VERSION.sdk.tar.xz
cp -r freebsd$VERSION.sdk.32/usr/lib32/*  /usr/cross-freebsd-32/i386-pc-freebsd$VERSION/lib
cp -r freebsd$VERSION.sdk/usr/include/*  /usr/cross-freebsd-32/i386-pc-freebsd$VERSION/include
./symlink32.h
