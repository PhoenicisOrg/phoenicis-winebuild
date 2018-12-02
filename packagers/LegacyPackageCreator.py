import pathlib
import shutil
import tempfile

from core.Process import run

"""
    Convert .tar.gz generated package to a PlayOnLinux / PlayOnMac < 4.3 compatible package.
    Deprecated
"""
class LegacyPackageCreator:
    def convert(self, package, os, arch, version):
        version_without_wine = version[5:]
        pol_name = ("PlayOnLinux-%s-%s-%s.pol") % (version, os, arch)
        with tempfile.TemporaryDirectory() as tmp_directory:
            playonlinux_path = tmp_directory + "/playonlinux"
            pathlib.Path(playonlinux_path).mkdir(parents=True, exist_ok=True)
            pathlib.Path(tmp_directory + "/files").mkdir(parents=True, exist_ok=True)
            with open(playonlinux_path + "/main", "w") as main_file:
                main_file.write("""#!/bin/bash
if [ "$PLAYONLINUX" = "" ]
then
        exit 0
fi

source "$PLAYONLINUX/lib/sources"

mkdir -p "$REPERTOIRE/wine/""" + os + "-" + arch + """/""" + version_without_wine + """"
cd "$REPERTOIRE/wine/""" + os + "-" + arch + """/""" + version_without_wine + """"

tar -xvf "$SCRIPT_DIRECTORY/wine.tar.gz"

exit""")
            shutil.copy(package, tmp_directory + "/files/wine.tar.gz")
            run(["tar", "czvf", pol_name, "-C", tmp_directory, "."])
