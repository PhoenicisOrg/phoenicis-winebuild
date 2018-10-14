#!/usr/bin/env python
from wine.WineVersionFetcher import WineVersionFetcher
from wine.PhoenicisWineBuilder import PhoenicisWineBuilder

def input_from_choices(choices, text):
    print("Choices: " + ", ".join(choices))
    result = input(text)
    if(result not in choices):
        print("Invalid value")
        return input_from_choices(choices, text)
    return result

version = input_from_choices([version["name"] for version in WineVersionFetcher().fetch_versions(majors = [1, 2, 3])], "Please select a wine version to build: ")

arch = input_from_choices(["x86", "amd64"], "Choose an architecture: ")
os = input_from_choices(["linux", "darwin"], "Choose an OS: ")
distribution = input_from_choices(["upstream"], "Choose a distribution: ")

builder = PhoenicisWineBuilder()

builder.build(lambda: None, lambda e: print(e), distribution, version, os, arch)
