import pathlib, datetime

from builders.RuntimeBuilder import RuntimeBuilder
from core.Container import Container
from core.Environment import Environment
from storage.PackageStore import PackageStore


class PhoenicisRuntimeWinePackageCreator:
    def __init__(self):
        self._output_callback = None

    def with_output_callback(self, output_callback):
        self._output_callback = output_callback
        return self

    def build(self, operating_system, arch):
        runtime_path = PackageStore.get_runtimes_path()
        pathlib.Path(runtime_path).mkdir(parents=True, exist_ok=True)

        # FIXME: Put more abstraction here:
        if operating_system == "darwin":
            environment = "wine_osxcross"
            env_arch = "x86"
        else:
            environment = "wine"
            env_arch = arch

        environment = Environment(environment, "linux", env_arch)
        environment.build()

        container = Container(environment).with_output_callback(self._output_callback)

        try:
            container.start()
            builder = RuntimeBuilder(container)
            builder.build(operating_system, arch)
            builder.archive(runtime_path + ("/runtime-%s-%s-%s.tar.gz" % (operating_system, arch, datetime.datetime.now().strftime("%Y%m%d%H%M"))))
            builder.checksum()
        finally:
            print("Cleaning container")
            container.clean()
