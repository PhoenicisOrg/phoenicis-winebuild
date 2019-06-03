#!/usr/bin/env python
from packagers.PhoenicisRuntimeWinePackageCreator import PhoenicisRuntimeWinePackageCreator

builder = PhoenicisRuntimeWinePackageCreator()

builder.build("darwin", "x86")
