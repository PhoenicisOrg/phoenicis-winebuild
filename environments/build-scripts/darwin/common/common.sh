#!/bin/bash

prepare() {
  rm -r /src/
  rm -r /build/
  mkdir -p /src/
  mkdir -p /staging/include/
  mkdir -p /staging/lib32/
  mkdir -p /staging/lib64/

  cd /src/ || exit 1

  if [ "$VERSION" = "" ]; then
    echo "Please specify gnutls version (env VERSION)"
    exit 1
  fi

  if [ "$ARCH" = "" ]; then
    echo "Please specify architecture (env ARCH)"
    exit 1
  fi

  [ "$ARCH" = "i386" ] && LIB_DIRECTORY="lib32" && ABI="32"
  [ "$ARCH" = "x86_64" ] && LIB_DIRECTORY="lib64" && ABI="64"

  export LIB_DIRECTORY
  export ABI

  export CC="$ARCH-apple-darwin17-clang -L/opt/local/$LIB_DIRECTORY -stdlib=libc++ -I/opt/local/include"
  export CXX="$ARCH-apple-darwin17-clang++ -L/opt/local/$LIB_DIRECTORY -stdlib=libc++ -I/opt/local/include"

  MAJOR_VERSION="$(basename "$VERSION" | cut -d"." -f1,2)"
  export MAJOR_VERSION
  return 0
}

install-libs() {
  cd "/build/$ARCH/" || exit 3
  cp -r lib/* "/opt/local/$LIB_DIRECTORY" || exit 4
  cp -r include/* "/opt/local/include/" || exit 4
}

stage-libs() {
  mkdir -p "/staging/$LIB_DIRECTORY"
  cd "/build/$ARCH/" || exit 3
  cp -r lib/* "/staging/$LIB_DIRECTORY" || exit 4
  cp -r include/* "/staging/include/" || exit 4
}

install-staging-libs() {
  mv /staging/lib32/*  "/opt/local/lib32"
  mv /staging/lib64/*  "/opt/local/lib64"
  mv /staging/include/*  "/opt/local/include"
  return 0
}