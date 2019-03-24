#!/bin/bash
git clone "https://source.winehq.org/git/vkd3d.git/" "/root/vkd3d"

cd "/root/vkd3d"
git checkout -f "vkd3d-1.1"

export C_INCLUDE_PATH="/root/osxcross/target/macports/pkgs/opt/local/include/:/root/osxcross/target/macports/pkgs/opt/local/include/libxml2/:/root/vulkansdk-macos-1.1.101.0/macOS/include/:/root/SPIRV-Headers/include/:/root/SPIRV-Headers/include/spirv/"
export LIBRARY_PATH="/root/osxcross/target/macports/pkgs/opt/local/lib:/root/vulkansdk-macos-1.1.101.0/macOS/lib/"
export PATH="/root/wine-tools/tools/widl/:$PATH"

./autogen.sh || exit 1
./configure --host x86_64-apple-darwin15 --prefix="/" LFFLAGS=" -Wl,-rpath,/opt/x11/lib -L/root/osxcross/target/macports/pkgs/opt/local/lib -F/root/osxcross/target/macports/pkgs/opt/local/Library/Frameworks" || exit 2
make || exit 3
make install DESTDIR="/root/osxcross/target/macports/pkgs/opt/local/" || exit 4
libtool --finish /root/osxcross/target/macports/pkgs/opt/local/lib || exit 5
exit 0
