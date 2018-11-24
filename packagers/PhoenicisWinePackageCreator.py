import os, pathlib

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder
from storage.PackageStore import PackageStore

class PhoenicisWinePackageCreator:
    def __init__(self):
        self._output_callback = None

    def with_output_callback(self, output_callback):
        self._output_callback = output_callback
        return self

    def build(self, distribution, version, os, arch):
        pathlib.Path(PackageStore.get_binaries_path()).mkdir(parents=True, exist_ok=True)
        pathlib.Path(PackageStore.get_logs_path()).mkdir(parents=True, exist_ok=True)

        # FIXME: Put more abstraction here:
        if os == "darwin":
            environment = "wine_osxcross"
            builderPath = "builders/scripts/builder_darwin_x86_wine"
        else:
            environment = "wine"
            builderPath = "builders/scripts/builder_linux_x86_wine"

        directory = "-".join([distribution, os, arch])
        filename = "-".join(["phoenicis", version, distribution, os, arch])

        pathlib.Path(PackageStore.get_logs_path() + "/" + directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path(PackageStore.get_binaries_path() + "/" + directory).mkdir(parents=True, exist_ok=True)

        environment = Environment(environment, "linux", arch)
        environment.build()

        container = Container(environment).with_log_file(
            PackageStore.get_logs_path() + "/" + directory + "/" + filename + ".log").with_output_callback(self._output_callback)

        try:
            container.start()
            builder = WineBuilder(container)
            builder.build(builderPath, version, distribution=distribution)
            builder.archive(PackageStore.get_binaries_path() + "/" + directory + "/" + filename + ".tar.gz")
            builder.checksum()
        finally:
            container.clean()


