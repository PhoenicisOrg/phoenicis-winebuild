#!/usr/bin/env python
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator

builder = PhoenicisWinePackageCreator()

builder.build("upstream", "winecx-4.0", "linux", "x86")
