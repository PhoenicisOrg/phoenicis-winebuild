from hooks.AbstractHook import AbstractHook


class AddProtonIncludes(AbstractHook):
    def builder(self):
        return "wine"

    def event(self):
        return "after-git"

    def patch(self, container, operating_system, arch, version, distribution):
        container.run(["git", "clone", "--progress", "https://github.com/ValveSoftware/Proton/", "/root/proton"])
        container.env("C_INCLUDE_PATH", "/root/proton/contrib/include")
