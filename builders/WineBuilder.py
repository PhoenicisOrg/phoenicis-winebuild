import tempfile

from core.Container import Container
from core.Process import run


class WineBuilder:
    def __init__(self, container: Container, patches=[]):
        self.container = container
        self.patches = patches

    def prepare(self, version, distribution="upstream"):
        self.container.run(["git", "clone", "https://github.com/wine-mirror/wine", "/root/wine-git"])
        self.container.run(["git", "checkout", "-f", version], workdir="/root/wine-git")

        if distribution == "staging":
            self.container.run(["git", "clone", "https://github.com/wine-staging/wine-staging", "/root/wine-staging"])
            self.container.run(["git", "checkout", "-f", "v" + version], workdir="/root/wine-staging")
            self.container.run(["./patches/patchinstall.sh", "DESTDIR=\"/root/wine-git\"", "--all"], workdir="/root/wine-staging")

        self._apply_patches()

    def build(self, script, version, distribution="upstream"):
        self.prepare(version, distribution)
        self.container.run_script(script)

    def archive(self, local_file):
        with tempfile.TemporaryDirectory() as tmp_directory:
            self.container.get_file("/root/wine/", tmp_directory + "/archive.tar.gz")
            run(["tar", "xf", tmp_directory + "/archive.tar.gz", "-C", tmp_directory])
            run(["tar", "-C", tmp_directory + "/wine", "-czvf", local_file, "./"])

    def _apply_patches(self):
        for patch in self.patches:
            self._apply_patch(patch)

    def _apply_patch(self, patch):
        self.container.run(["mkdir", "-p", "/root/patches"])
        self.container.put_directory("patches/" + patch, "/root/patches/" + patch)
        self.container.run(["sh", "-c", "git apply /root/patches/" + patch + "/*.patch"], workdir="/root/wine-git")
