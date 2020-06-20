from hooks.AbstractHook import AbstractHook


class ApplyDosboxPatch(AbstractHook):
    def builder(self):
        return "wine"

    def event(self):
        return "after-build"

    def patch(self, container, operating_system, arch, version, distribution):
        container.run(["git", "clone", "--progress", "https://github.com/PhoenicisOrg/phoenicis-wine-dosbox_support", "/root/wine-dosbox-wrapper"])
        container.run(["bash", "patch-wine.sh", "/root/wine/"], workdir="/root/wine-dosbox-wrapper")

        if operating_system == "darwin":
            self._install_darwin_dosbox(container)

        if operating_system == "linux":
            self._install_linux_dosbox(container)

    def _install_darwin_dosbox(self, container):
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/bin/dosbox", "/root/wine/bin/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libSDL_sound-1.0.1.dylib", "/root/wine/lib/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libSDL-1.2.0.dylib", "/root/wine/lib/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libpng16.16.dylib", "/root/wine/lib/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libz.1.dylib", "/root/wine/lib/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libSDL_net-1.2.0.dylib", "/root/wine/lib/"])
        container.run(["cp", "/root/osxcross/target/macports/pkgs/opt/local/lib/libX11.6.dylib", "/root/wine/lib/"])

    def _install_linux_dosbox(self, container):
        container.run(["cp", "/usr/bin/dosbox", "/root/wine/bin/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libSDL-1.2.so.0", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libSDL_net-1.2.so.0", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libSDL_sound-1.0.so.1", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libcaca.so.0", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/sse2/libspeex.so.1", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libvorbis.so.0", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libvorbisenc.so.2", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libvorbisfile.so.3", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libogg.so.0", "/root/wine/lib/"])
        container.run(["cp", "/usr/lib/i386-linux-gnu/libFLAC.so", "/root/wine/lib/"])
