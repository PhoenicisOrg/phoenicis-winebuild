from hooks.AbstractHook import AbstractHook


class InstallDosbox(AbstractHook):
    def builder(self):
        return "wine"

    def event(self):
        return "after-git"

    def patch(self, container, operating_system, arch, version, distribution):
        if operating_system == "darwin":
            container.run(["omp", "install", "-32", "dosbox"])

        if operating_system == "linux":
            container.run(["apt-get", "-y", "install", "dosbox"])