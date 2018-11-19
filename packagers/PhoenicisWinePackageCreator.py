import os, pathlib

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder


class PhoenicisWinePackageCreator:
    def __init__(self):
        self._output_callback = None

    def with_output_callback(self, output_callback):
        self._output_callback = output_callback
        return self

    def build(self, distribution, version, os, arch):
        pathlib.Path("dist/binaries").mkdir(parents=True, exist_ok=True)
        pathlib.Path("dist/logs").mkdir(parents=True, exist_ok=True)

        # FIXME: Put more abstraction here:
        if (os == "darwin"):
            environment = "wine_osxcross"
            builderPath = "builders/scripts/builder_darwin_x86_wine"
        else:
            environment = "wine"
            builderPath = "builders/scripts/builder_linux_x86_wine"

        directory = "-".join([distribution, os, arch])
        filename = "-".join(["phoenicis", version, os, arch])

        pathlib.Path("dist/logs/" + directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path("dist/binaries/" + directory).mkdir(parents=True, exist_ok=True)

        environment = Environment(environment, "linux", arch)
        environment.build()

        container = Container(environment).with_log_file(
            "dist/logs/" + directory + "/" + filename + ".log").with_output_callback(self._output_callback)

        try:
            container.start()
            builder = WineBuilder(container)
            builder.build(builderPath, version, distribution=distribution)
            builder.archive("dist/binaries/" + directory + "/" + filename + ".tar.gz")
        finally:
            container.clean()
