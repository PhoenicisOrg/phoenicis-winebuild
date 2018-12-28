from hooks.AbstractHook import AbstractHook


class ApplyWineStagingPatches(AbstractHook):
    def builder(self):
        return "wine"

    def event(self):
        return "after-git"

    def patch(self, container, operating_system, arch, version, distribution):
        container.run(["git", "clone", "--progress", "https://github.com/wine-staging/wine-staging", "/root/wine-staging"])
        container.run(["git", "checkout", "-f", version.replace("wine-", "v")], workdir="/root/wine-staging")
        container.run(["./patches/patchinstall.sh", "DESTDIR=/root/wine-git", "--all"], workdir="/root/wine-staging")
