#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine", "linux", "amd64")
environment.build()


container = Container(environment)
container.start()

builder = WineBuilder(container)
builder.build("builders/scripts/builder_linux_amd64_wine", "wine-3.21")
builder.archive("wine.tar.gz")

container.clean()
