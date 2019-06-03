#!/bin/bash

olddir="$PWD"
cd "$(dirname "$0")"
scriptDir="$PWD"

cd "$olddir"
"$scriptDir/wine64" "../hangover/qemu-x86_64.exe.so" "$@"