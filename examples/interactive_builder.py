#!/usr/bin/env python
from wine.WineVersionFetcher import WineVersionFetcher
from packagers.PhoenicisWinePackageCreator import PhoenicisWinePackageCreator


def input_from_choices(choices, text):
    print("Choices: " + ", ".join(choices))
    result = input(text)
    if result not in choices:
        print("Invalid value")
        return input_from_choices(choices, text)
    return result


version = input_from_choices([version["name"] for version in WineVersionFetcher().fetch_versions(majors=[1, 2, 3, 4, 5, 6])],
                             "Please select a wine version to build: ")

arch = input_from_choices(["x86", "amd64"], "Choose an architecture: ")
os = input_from_choices(["linux", "darwin"], "Choose an OS: ")
distribution = input_from_choices(["upstream", "staging", "cx", "dos_support", "proton"], "Choose a distribution: ")

builder = PhoenicisWinePackageCreator()

builder.build(distribution, version, os, arch)
