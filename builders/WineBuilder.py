class WineBuilder:
    def __init__(self, container):
        self.container = container

    def build(self, script, version):
        self.container.run(["git", "clone", "git://source.winehq.org/git/wine.git", "/root/wine-git"])
        self.container.run(["git", "checkout", "-f", version], workdir = "/root/wine-git")
        self.container.run_script(script)

    def archive(self, local_file = None):
        self.container.run(["tar", "czvf", "/root/wine.tar.gz", "."], workdir = "/root/wine")
        self.container.get_file("/root/wine.tar.gz", local_file)
