class WineBuilder:
    def __init__(self, container):
        self.container = container

    def build(self, script, version):
        self.container.run(["git", "clone", "git://source.winehq.org/git/wine.git", "/root/wine-git"])
        self.container.run(["git", "checkout", "-f", version, "--workdir", "/root/wine-git"])

        self.container.run_script(script)
