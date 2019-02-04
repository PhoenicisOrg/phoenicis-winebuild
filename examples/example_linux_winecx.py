#!/usr/bin/env python
from wine.WineVersionFetcher import WineVersionFetcher
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator

builder = PhoenicisWinePackageCreator()

builder.build("cx", "winecx-18.1.0", "linux", "x86")
