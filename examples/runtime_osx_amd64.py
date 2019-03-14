#!/usr/bin/env python
from builders.RuntimeBuilder import RuntimeBuilder
from core.Container import Container
from core.Environment import Environment

environment = Environment("wine_osxcross", "linux", "x86")
environment.build()

container = Container(environment)
container.start()

builder = RuntimeBuilder(container)
builder.build("darwin", "amd64")
builder.archive("runtime.tar.gz")
