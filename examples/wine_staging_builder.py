#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine", "linux", "x86")
environment.build()

container = Container(environment)
container.start()


builder = WineBuilder(container)
builder.build("linux", "x86", "wine-3.8", "staging")
builder.archive("wine-staging.tar.gz")

container.clean()