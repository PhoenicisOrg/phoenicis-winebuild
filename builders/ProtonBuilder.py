import tempfile

from core.Container import Container
from core.Process import run

class ProtonBuilder:
    def __init__(self, container: Container, patches = []):
        self.container = container
        self.patches = patches

    def prepare(self, version):
        self.container.run(["git", "clone", "https://github.com/ValveSoftware/steam-runtime.git", "/root/steam-runtime"])
        self.container.run(["git", "checkout", "-b", "wip-docker", "origin/wip-docker"], workdir = "/root/steam-runtime")
        self.container.run(["git", "clone", "https://github.com/ValveSoftware/Proton", "/root/proton-git"])
        self.container.run(["git", "checkout", "-f", version], workdir = "/root/proton-git")
        self.container.run(["git", "submodule", "update", "--init"], workdir="/root/proton-git")
        self._apply_patches()

    def build(self, script, version):
        self.prepare(version)
        self.container.run_script(script)

    def archive(self, local_file):
        with tempfile.TemporaryDirectory() as tmp_directory:
            self.container.get_file("/root/proton/", tmp_directory + "/archive.tar.gz")
            run(["tar", "xf", tmp_directory + "/archive.tar.gz", "-C", tmp_directory])
            run(["tar", "-C", tmp_directory + "/proton", "-czvf", local_file, "./"])

    def _apply_patches(self):
        for patch in self.patches:
            self._apply_patch(patch)

    def _apply_patch(self, patch):
        self.container.run(["mkdir", "-p", "/root/patches"])
        self.container.put_directory("patches/" + patch, "/root/patches/" + patch)
        self.container.run(["sh", "-c", "git apply /root/patches/"+patch+"/*.patch"], workdir = "/root/proton-git")
