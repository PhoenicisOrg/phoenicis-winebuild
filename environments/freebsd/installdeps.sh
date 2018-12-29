#!/bin/bash
url="http://pkg.freebsd.org/freebsd:$VERSION:x86:64/latest/All/"
installdeps(){
	mkdir tmp/
	cd tmp/
	wget $url$1
	tar -xf $1
	cp -r usr/local/lib/* /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/lib
	cp -r usr/local/include/* /usr/cross-freebsd/x86_64-pc-freebsd$VERSION/include
	cd ../
	rm -rf tmp/
}
