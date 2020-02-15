#!/bin/bash
# This script is adapted from wine-staging work
# It compiles a compiler that support ms_hook_prologue attribute

mkdir -p "/root/clang_wine32/"
cd "/root/clang_wine32/"
apt-get -y install devscripts wget

llvmBaseUrl="http://ftp.debian.org/debian/pool/main/l/llvm-toolchain-8/"
llvmMainVersion="8_8.0.1"
llvmVersion="4"

wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion-$llvmVersion.dsc"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-clang-tools-extra.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-clang.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-compiler-rt.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-lldb.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-libcxx.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-libcxxabi.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-lld.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-openmp.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig-polly.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion.orig.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-$llvmMainVersion-$llvmVersion.debian.tar.xz"

dpkg-source -x llvm-toolchain-$llvmMainVersion-$llvmVersion.dsc

cd llvm-toolchain-7-7.0.1/
cat ../0003-Add-Wine32-Support-Full.patch | patch -p1
mk-build-deps -i -r -t "apt-get -y" debian/control

DEB_BUILD_OPTIONS=nocheck debuild -us -uc -nc -b -j3
exit 0