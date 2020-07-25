import tempfile, hashlib, os

from core.Container import Container
from core.Process import run
from hooks import AbstractHook

from typing import List


class WineBuilder:
    def __init__(self, container: Container, patches=None, hooks=None, builder_suffix=None):
        self.container = container
        self.patches = patches or []
        self.hooks: List[AbstractHook] = hooks or []
        self.builder_suffix = builder_suffix
        self._local_archive = None

    def prepare(self, operating_system, arch, version, distribution, repository, clone = True):
        if clone:
           self.container.run(["git", "clone", "--progress", repository, "/root/wine-git"])
           self.container.run(["git", "checkout", "-f", version], workdir="/root/wine-git")

        self._apply_hooks("after-git", operating_system, arch, version, distribution)

        self._apply_patches(operating_system, arch)

    def _apply_hooks(self, event, operating_system, arch, version, distribution):
        for hook in self.hooks:
            if hook.event() == event:
                hook.patch(self.container, operating_system, arch, version, distribution)

    def build(self, operating_system, arch, version, distribution="upstream",
              repository="https://github.com/wine-mirror/wine", clone = True):
        script = "builders/scripts/builder_%s_%s_wine" % (operating_system, arch)

        if self.builder_suffix is not None:
            script = script + "_" + self.builder_suffix

        self.prepare(operating_system, arch, version, distribution, repository, clone)
        self.container.run_script(script)
        self._apply_hooks("after-build", operating_system, arch, version, distribution)

    def archive(self, local_file):
        with tempfile.TemporaryDirectory() as tmp_directory:
            self.container.get_file("/root/wine/", tmp_directory + "/archive.tar.gz")
            self._local_archive = local_file
            run(["tar", "xf", tmp_directory + "/archive.tar.gz", "-C", tmp_directory])
            run(["tar", "-C", tmp_directory + "/wine", "-czvf", local_file, "./"])

    def _apply_patches(self, operating_system, architecture):
        for patch in self.patches:
            if type(patch) == str:
                self._apply_patch({
                    "name": patch["name"]
                })
            if type(patch == dict):
                if operating_system in patch["operatingSystems"] and architecture in patch["architectures"]:
                    self._apply_patch(patch)


    def _apply_patch(self, patch):
        self.container.run(["mkdir", "-p", "/root/patches"])

        if "git" in patch:
            patchGit = patch["git"]
            gitPatchDirectory = "/root/patches/%s" % patch["name"]
            gitCloneCommand = "git clone %s %s" % (patchGit["url"], gitPatchDirectory)
            gitCheckoutCommand = "git checkout -f %s" % patchGit["branch"]

            self.container.run(["sh", "-c", gitCloneCommand], workdir="/root/wine-git")
            self.container.run(["sh", "-c", gitCheckoutCommand], workdir=gitPatchDirectory)
            self.container.run(["sh", "-c", "git apply --3way " + gitPatchDirectory + "/" + patchGit["directory"] +"/*.diff"], workdir="/root/wine-git")
        else:
            self.container.put_directory("patches/" + patch["name"], "/root/patches/" + patch["name"])
            self.container.run(["sh", "-c", "git apply --3way /root/patches/" + patch["name"] + "/*.diff"], workdir="/root/wine-git")

    def checksum(self):
        if self._local_archive is not None:
            sha1sum = hashlib.sha1()
            with open(self._local_archive, 'rb') as source:
                block = source.read(2 ** 16)
                while len(block) != 0:
                    sha1sum.update(block)
                    block = source.read(2 ** 16)

            resulting_checksum = sha1sum.hexdigest()
            with open(self._local_archive + ".sha1", 'w') as checksum_file:
                checksum_file.write("%s  %s" % (resulting_checksum, os.path.basename(self._local_archive)))
