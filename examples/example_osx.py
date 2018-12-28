#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine_osxcross", "linux", "x86")
environment.build()

container = Container(environment)
container.start()


builder = WineBuilder(container)
builder.build("darwin_x86", "wine-3.18")
#builder.archive("wine-3.18-darwin-x86.tar.gz")
