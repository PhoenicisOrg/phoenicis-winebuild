#!/usr/bin/env python

from core.Container import Container
from core.Environment import Environment
from builders.ProtonBuilder import ProtonBuilder

environment = Environment("proton", "linux", "amd64")
environment.build()

container = Container(environment).with_log_file("test_log.log")


container.start()

builder = ProtonBuilder(container)
builder.build("builders/scripts/builder_linux_amd64_proton", "proton_3.16")
builder.archive("proton.tar.gz")

# container.clean()
