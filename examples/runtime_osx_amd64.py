#!/usr/bin/env python
from packagers.PhoenicisRuntimeWinePackageCreator import PhoenicisRuntimeWinePackageCreator

builder = PhoenicisRuntimeWinePackageCreator()

builder.build("darwin", "amd64")
