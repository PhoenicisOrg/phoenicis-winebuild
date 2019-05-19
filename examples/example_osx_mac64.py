#!/usr/bin/env python
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator

builder = PhoenicisWinePackageCreator()

builder.build("upstream", "wine-4.0.1", "darwin", "mac64")
