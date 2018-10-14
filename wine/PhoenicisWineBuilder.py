import os, pathlib

from core.Container import Container
from core.Environment import Environment
from builders.WineBuilder import WineBuilder

class PhoenicisWineBuilder:
    def build(self, callback, error_callback, distribution, version, os, arch):
        pathlib.Path("dist/binaries").mkdir(parents=True, exist_ok=True)
        pathlib.Path("dist/logs").mkdir(parents=True, exist_ok=True)

        try:
            if(distribution == "upstream"):
                self.build_upstream(callback, version, os, arch)
        except Exception as e:
            error_callback(e)

    def build_upstream(self, callback, version, os, arch):
        # FIXME: Put more abstraction here:
        if(os == "darwin"):
            environment = "wine_osxcross"
            builderPath = "builders/builder_darwin_x86_wine"
        else:
            environment = "wine"
            builderPath = "builders/builder_linux_x86_wine"

        directory = "-".join(["upstream", os, arch])
        filename = "-".join(["phoenicis", version, os, arch])

        pathlib.Path("dist/logs/" + directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path("dist/binaries/" + directory).mkdir(parents=True, exist_ok=True)

        environment = Environment(environment, "linux", arch)
        environment.build()

        container = Container(environment).with_log_file("dist/logs/" + directory + "/" + filename + ".log")
        try:
            container.start()
            builder = WineBuilder(container)
            builder.build(builderPath, version)
            builder.archive("dist/binaries/"+directory+"/"+filename+".tar.gz")
            callback()
        finally:
            container.clean()
