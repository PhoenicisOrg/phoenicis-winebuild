#!/usr/bin/env python

import argparse
import os
import sys

from builders.WineBuilder import WineBuilder
from core.Container import Container
from core.Environment import Environment


def info(info):
    print(info)


def fatal(error):
    print(error)
    sys.exit(1)


parser = argparse.ArgumentParser(description='Add some integers.')

parser.add_argument('--wine-src', default=None,
                    help='wine source directory (default: current directory)')

parser.add_argument('--apply-patches', default=None,
                    help='apply wine patches to the current root (default: no patches)')

parser.add_argument('--environment', help='Environment to use')

parser.add_argument('--os', help='Target OS to build')

parser.add_argument('--architecture', help='Target architecture to build')

parser.add_argument('--build', help="Build", action="store_true")

parser.add_argument('--no-clean', help="Don't clean container after building (useful if you want to debug the process)", action="store_true")

args = parser.parse_args()

if args.environment is None:
    fatal("You need to provide a valid environment (ex: --environment=wine_osxcross/linux/amd64)")

wine_source = args.wine_src if args.wine_src is not None else os.getcwd()
patches = [{
    "name": patch,
    "operatingSystems": args.os,
    "architecture": args.architecture
}  for patch in args.apply_patches] if args.apply_patches is not None else None

try:
    environment = args.environment.split("/")
    build_environment = Environment(environment[0], environment[1], environment[2])
    info("Building environment...")
    build_environment.build()
    container = Container(build_environment)
    container.with_mount({
        "src": wine_source,
        "dest": "/root/wine-git",
        "mode": "rw"
    })
    container.start()

    builder = WineBuilder(container, patches)

    if patches is not None:
        builder.prepare(args.os, args.architecture, None, None, None, clone=True)

    if args.build:
        builder.do_build(args.os, args.architecture)

    if not args.no_clean:
        container.clean()

except IndexError:
    fatal("You need to provide a valid environment (ex: --environment=wine_osxcross/linux/amd64)")

