#!/bin/bash
cd /root
wget https://ftp.gnu.org/gnu/binutils/binutils-2.31.tar.xz
tar -xf binutils-2.31.tar.xz
cd /root/binutils-2.31
./configure --enable-libssp --enable-gold --enable-ld --target=x86_64-pc-freebsd$VERSION --prefix=/usr/cross-freebsd
make
make install
cd /root
rm -rf /root/binutils-2.31

wget https://ftp.gnu.org/gnu/gmp/gmp-6.1.2.tar.xz
tar -xf gmp-6.1.2.tar.xz
cd /root/gmp-6.1.2
./configure --prefix=/usr/cross-freebsd --enable-shared --enable-static --enable-fft --enable-cxx --host=x86_64-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/gmp-6.1.2

wget https://ftp.gnu.org/gnu/mpfr/mpfr-4.0.1.tar.xz
tar -xf mpfr-4.0.1.tar.xz
cd /root/mpfr-4.0.1
./configure --prefix=/usr/cross-freebsd --with-gnu-ld --with-gmp=/usr/cross-freebsd --enable-static --enable-shared --host=x86_64-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/mpfr-4.0.1

wget https://ftp.gnu.org/gnu/mpc/mpc-1.1.0.tar.gz
tar -xf mpc-1.1.0.tar.gz
cd /root/mpc-1.1.0
./configure --prefix=/usr/cross-freebsd --with-gnu-ld --with-gmp=/usr/cross-freebsd --with-mpfr=/usr/cross-freebsd --enable-static --enable-shared --host=x86_64-pc-freebsd$VERSION
make
make install
cd /root
rm -rf /root/mpc-1.1.0

wget https://ftp.gnu.org/gnu/gcc/gcc-$GCCVERSION/gcc-$GCCVERSION.tar.gz
tar -xf gcc-$GCCVERSION.tar.gz
mkdir objdir
cd /root/objdir
../gcc-$GCCVERSION/configure --without-headers --with-gnu-as --with-gnu-ld --enable-languages=c,c++ --disable-nls --enable-libssp --enable-gold --enable-ld --target=x86_64-pc-freebsd$VERSION --prefix=/usr/cross-freebsd --with-gmp=/usr/cross-freebsd --with-mpc=/usr/cross-freebsd --with-mpfr=/usr/cross-freebsd --disable-libgomp
LD_LIBRARY_PATH=/usr/cross-freebsd/lib make
make install
cd /root
rm -rf /root/gcc-$GCCVERSION
