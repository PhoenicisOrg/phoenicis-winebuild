#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine", "linux", "amd64")
environment.build()


container = Container(environment)
container.start()

builder = WineBuilder(container)
builder.build("linux", "amd64", "wine-3.21")
builder.archive("wine.tar.gz")

container.clean()
