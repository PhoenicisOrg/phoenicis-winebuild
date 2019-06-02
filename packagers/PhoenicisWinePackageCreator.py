import pathlib, traceback

from builders.WineBuilder import WineBuilder
from core.ConfigurationReader import ConfigurationReader
from core.Container import Container
from core.Environment import Environment
from storage.PackageStore import PackageStore


class PhoenicisWinePackageCreator:
    def __init__(self):
        self._output_callback = None

    def with_output_callback(self, output_callback):
        self._output_callback = output_callback
        return self

    def fetch_distribution(self, distribution_name):
        distributions = ConfigurationReader().read("distributions")
        for distribution in distributions:
            if distribution["name"] == distribution_name:
                return distribution

    def build(self, distribution, version, operating_system, arch):
        distribution_parameters = self.fetch_distribution(distribution)

        pathlib.Path(PackageStore.get_binaries_path()).mkdir(parents=True, exist_ok=True)
        pathlib.Path(PackageStore.get_logs_path()).mkdir(parents=True, exist_ok=True)

        # FIXME: Put more abstraction here:

        environmentSuffix = ""
        if "environmentSuffix" in distribution_parameters:
            environmentSuffix = "_" + distribution_parameters["environmentSuffix"]

        if operating_system == "darwin":
            environment = "wine_osxcross" + environmentSuffix
            env_arch = "amd64"
        else:
            environment = "wine" + environmentSuffix
            env_arch = arch

        directory = "-".join([distribution, operating_system, arch])
        filename = "-".join(["PlayOnLinux", version, distribution, operating_system, arch])

        pathlib.Path(PackageStore.get_logs_path() + "/" + directory).mkdir(parents=True, exist_ok=True)
        pathlib.Path(PackageStore.get_binaries_path() + "/" + directory).mkdir(parents=True, exist_ok=True)

        environment = Environment(environment, "linux", env_arch)
        environment.build()

        container = Container(environment).with_log_file(
            PackageStore.get_logs_path() + "/" + directory + "/" + filename + ".log").with_output_callback(self._output_callback)

        scriptSuffix = None
        if "scriptSuffix" in distribution_parameters:
            scriptSuffix = distribution_parameters["scriptSuffix"]

        try:
            container.start()
            builder = WineBuilder(container, distribution_parameters["patches"], self.create_hooks(distribution_parameters["hooks"]), scriptSuffix)
            builder.build(operating_system, arch, version, distribution, distribution_parameters["source"])
            builder.archive(PackageStore.get_binaries_path() + "/" + directory + "/" + filename + ".tar.gz")
            builder.checksum()
        except:
            traceback.print_exc()
        finally:
            print("Cleaning container")
            container.clean()

    def create_hooks(self, hooks):
        hooks_instances = []

        for hook_config in hooks:
            hook_name = hook_config["template"]
            hook_module =  __import__("hooks.%s" % hook_name, fromlist=["hooks"])
            hook_clazz = getattr(hook_module, hook_name.split(".")[-1:][0])
            hooks_instances += [hook_clazz()]

        return hooks_instances


