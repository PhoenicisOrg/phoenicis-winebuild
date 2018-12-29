#!/bin/bash
# This script is adapted from wine-staging work
# It compiles a compiler that support ms_hook_prologue attribute

mkdir -p "/root/clang_ms_hook_prologue/"
cd "/root/clang_ms_hook_prologue/"
apt-get -y install devscripts wget

llvmBaseUrl="http://http.debian.net/debian/pool/main/l/llvm-toolchain-3.8"
llvmVersion="24"

wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1-$llvmVersion.dsc"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig-clang-tools-extra.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig-clang.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig-compiler-rt.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig-lldb.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig-polly.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1.orig.tar.bz2"
wget "$llvmBaseUrl/llvm-toolchain-3.8_3.8.1-$llvmVersion.debian.tar.xz"

cat << EOF > checksums
d223323976e99805f0c3a3187f389d768131970b9ba74a44c5375519d26cdc70  llvm-toolchain-3.8_3.8.1-24.debian.tar.xz
f61be4a4e06656acb88d6f1a607f4e415c0ee40ee0f8e88a96f92ba3e1a8e6df  llvm-toolchain-3.8_3.8.1-24.dsc
788500834305622c7189b1ca9e328f1871b92b234c9397ac7fdde9ca2361dbfc  llvm-toolchain-3.8_3.8.1.orig-clang-tools-extra.tar.bz2
3edb39a9df41cc696c7376d006f4b691f1f91a5e828de842aa5a35375cbe0737  llvm-toolchain-3.8_3.8.1.orig-clang.tar.bz2
3e69e63516b51a0158ad1845b4a98a78bb9f93df5642b7cdf04b3e6e328abe31  llvm-toolchain-3.8_3.8.1.orig-compiler-rt.tar.bz2
ff85776e2157f45aa04b03fe34cdd880f8567ae41cb05964dc26a3cb9a252e19  llvm-toolchain-3.8_3.8.1.orig-lldb.tar.bz2
317e850d90cc9b63e732cc9e95c071fef5bf5e364dcc568aaf56cd1a0e76be09  llvm-toolchain-3.8_3.8.1.orig-polly.tar.bz2
49bb76301db200454025966887960741a2756a7d0bdb2c44a69436859357c73c  llvm-toolchain-3.8_3.8.1.orig.tar.bz2
EOF

dpkg-source -x llvm-toolchain-3.8_3.8.1-$llvmVersion.dsc

# wget https://raw.githubusercontent.com/wine-compholio/wine-packaging/master/packaging-other/clang/0001-Add-ms_hook_prologue-attribute.patch

cd llvm-toolchain-3.8-3.8.1
cat ../*.patch | patch -p1
mk-build-deps -i -r -t "apt-get -y" debian/control
DEB_BUILD_OPTIONS=nocheck debuild -us -uc -b -j3
exit 2