class WineBuilder:
    def __init__(self, container, patches = []):
        self.container = container
        self.patches = patches

    def build(self, script, version):
        self.container.run(["git", "clone", "git://source.winehq.org/git/wine.git", "/root/wine-git"])
        self._apply_patches()
        self.container.run(["git", "checkout", "-f", version], workdir = "/root/wine-git")
        self.container.run_script(script)

    def archive(self, local_file = None):
        self.container.run(["tar", "czvf", "/root/wine.tar.gz", "."], workdir = "/root/wine")
        self.container.get_file("/root/wine.tar.gz", local_file)

    def _apply_patches(self):
        for patch in self.patches:
            self._apply_patch(patch)

    def _apply_patch(self, patch):
        self.container.run(["mkdir", "-p", "/root/patches"])
        self.container.put("patches/" + patch, "/root/patches/")
        self.container.run(["sh", "-c", "git apply /root/patches/"+patch+"/*.patch"], workdir = "/root/wine-git")
