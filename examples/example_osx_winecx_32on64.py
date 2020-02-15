#!/usr/bin/env python
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator

builder = PhoenicisWinePackageCreator()

builder.build("cx", "winecx-19.0.0", "darwin", "x86on64")
