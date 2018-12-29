#!/usr/bin/env bash

# Copyright 2018, Phoenicis Team, Quentin Pâris
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
# THE USE OR OTHER DEALINGS IN THE SOFTWARE.

fix_imports () {
  [[ "$1" = "" ]] && echo "Please set a library name" && return
  echo "Fixing $1... "
  install_name_tool -id "$1" "$1"

  for lib in $(otool -L $1 |grep /opt/local --color=never|cut -d"(" -f1|xargs); do
   basename="$(basename $lib)"
   install_name_tool -change "/opt/local/lib/$basename" "@loader_path/$basename" $1
   echo "/opt/local/lib/$basename -> @loader_path/$basename"
  done

  echo "Done"
  echo ""
}

usage () {
    echo "fix_imports.sh /destination/of/wine/installation"
}

[[ "$1" = "" ]] && usage && exit

cd "$1" || exit 2

cd "$1/lib" || exit 2
for lib in *.dylib; do fix_imports "$lib"; done

cd "$1/lib/wine" || exit 2
for lib in *.so; do fix_imports "$lib"; done
