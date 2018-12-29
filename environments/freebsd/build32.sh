#!/bin/bash
cd /root
tar -xf binutils-2.31.tar.xz
cd /root/binutils-2.31
./configure --enable-libssp --enable-gold --enable-ld --target=i386-pc-freebsd$VERSION --prefix=/usr/cross-freebsd-32
make
make install
cd /root
rm -rf /root/binutils-2.31

tar -xf gmp-6.1.2.tar.xz
cd /root/gmp-6.1.2
./configure --prefix=/usr/cross-freebsd-32 --enable-shared --enable-static --enable-fft --enable-cxx --host=i386-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/gmp-6.1.2

tar -xf mpfr-4.0.1.tar.xz
cd /root/mpfr-4.0.1
./configure --prefix=/usr/cross-freebsd-32 --with-gnu-ld --with-gmp=/usr/cross-freebsd-32 --enable-static --enable-shared --host=i386-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/mpfr-4.0.1

tar -xf mpc-1.1.0.tar.gz
cd /root/mpc-1.1.0
./configure --prefix=/usr/cross-freebsd-32 --with-gnu-ld --with-gmp=/usr/cross-freebsd-32 --with-mpfr=/usr/cross-freebsd-32 --enable-static --enable-shared --host=i386-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/mpc-1.1.0

tar -xf gcc-$GCCVERSION.tar.gz
mkdir objdir
cd /root/objdir
../gcc-$GCCVERSION/configure --without-headers --with-gnu-as --with-gnu-ld --enable-languages=c,c++ --disable-nls --enable-libssp --enable-gold --enable-ld --target=i386-pc-freebsd$VERSION --prefix=/usr/cross-freebsd-32 --with-gmp=/usr/cross-freebsd-32 --with-mpc=/usr/cross-freebsd-32 --with-mpfr=/usr/cross-freebsd-32 --disable-libgomp
LD_LIBRARY_PATH=/usr/cross-freebsd-32/lib make
make install
cd /root
rm -rf /root/gcc-$GCCVERSION
