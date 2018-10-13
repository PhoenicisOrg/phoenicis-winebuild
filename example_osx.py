#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine", "darwin", "x86")
environment.build()

container = Container(environment)
container.start()


builder = WineBuilder(container)
builder.build("builders/builder_darwin_x86_wine", "wine-3.0.3")
builder.archive("wine-3.0.3-darwin.tar.gz")
