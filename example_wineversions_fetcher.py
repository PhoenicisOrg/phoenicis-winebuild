#!/usr/bin/env python
from wine.WineVersionFetcher import WineVersionFetcher

wlf = WineVersionFetcher()
print(wlf.fetch_versions(majors = [3]))
