#!/usr/bin/env python

import argparse
import os
import sys

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

args = parser.parse_args()

if args.environment is None:
    fatal("You need to provide a valid environment (ex: --environment=wine_osxcross/linux/amd64)")

wine_source = args.wine_src if args.wine_src is not None else os.getcwd()

try:
    environment = args.environment.split("/")
    build_environment = Environment(environment[0], environment[1], environment[2])
    info("Building environment...")
    build_environment.build()
    container = Container(environment)
    container.with_mount({
        "src": wine_source,
        "dest": "/home/wine-git",
        "mode": "rw"
    })
    container.start()
except IndexError:
    fatal("You need to provide a valid environment (ex: --environment=wine_osxcross/linux/amd64)")


print(args.apply_patches)
print(wine_source)
