#!/bin/sh
mkdir -p /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/include
mkdir -p /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib

tar -xf freebsd$VERSION.sdk.tar.xz
cp -r freebsd$VERSION.sdk/usr/lib/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib
cp -r freebsd$VERSION.sdk/usr/include/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/include
cp -r freebsd$VERSION.sdk/lib/*  /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib

mkdir -p /usr/cross-freebsd/i386-pc-freebsd$VERSION/include
mkdir -p /usr/cross-freebsd/i386-pc-freebsd$VERSION/lib

tar -xf freebsd$VERSION.sdk.32.tar.xz
cp -r freebsd$VERSION.sdk.32/usr/lib32/*  /usr/cross-freebsd/i386-pc-freebsd$VERSION/lib
cp -r freebsd$VERSION.sdk/usr/include/*  /usr/cross-freebsd/i386-pc-freebsd$VERSION/include
