import tempfile, hashlib, os

from core.Container import Container
from core.Process import run
from hooks import AbstractHook

from typing import List


class RuntimeBuilder:
    def __init__(self, container: Container, patches=None, hooks=None):
        self.container = container
        self.patches = patches or []
        self.hooks: List[AbstractHook] = hooks or []
        self._local_archive = None


    def build(self, operating_system, arch):
        script = "builders/scripts/builder_%s_%s_runtime" % (operating_system, arch)
        self.container.run_script(script)

    def archive(self, local_file):
        with tempfile.TemporaryDirectory() as tmp_directory:
            self.container.get_file("/root/runtime/", tmp_directory + "/archive.tar.gz")
            self._local_archive = local_file
            run(["tar", "xf", tmp_directory + "/archive.tar.gz", "-C", tmp_directory])
            run(["tar", "-C", tmp_directory + "/runtime", "-czvf", local_file, "./"])

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
