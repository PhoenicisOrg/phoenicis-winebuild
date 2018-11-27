#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

environment = Environment("wine", "linux", "x86")
environment.build()

container = Container(environment).with_log_file("test_log.log")


container.start()

builder = WineBuilder(container)
builder.build("builders/scripts/builder_linux_x86_wine", "wine-3.21")
builder.archive("wine.tar.gz")

container.clean()
