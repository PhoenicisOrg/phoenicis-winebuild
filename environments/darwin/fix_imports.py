#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Tool to fixup imports in Macho files.
#
# Copyright (C) 2015 Michael Müller
# Copyright (C) 2016 Sebastian Lackner
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA
#

import argparse
import os
import stat
import subprocess


# Load list of files into a set
def load_filelist(path):
    files = set()

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("./"):
                line = line[1:]
            assert line[0] == "/"
            files.add(line)

    return files


# Check if a file is a mach executable
def is_mach_executable(path):
    with open(path, "rb") as f:
        buf = f.read(16)

    if buf[0:4] != "\xCE\xFA\xED\xFE" and buf[0:4] != "\xCF\xFA\xED\xFE": return False
    if buf[4:8] != "\x07\x00\x00\x00" and buf[4:8] != "\x07\x00\x00\x01": return False
    return (buf[12:16] == "\x02\x00\x00\x00")


# Check if a file is a mach dylib
def is_mach_dylib(path):
    with open(path, "rb") as f:
        buf = f.read(16)

    if buf[0:4] != "\xCE\xFA\xED\xFE" and buf[0:4] != "\xCF\xFA\xED\xFE": return False
    if buf[4:8] != "\x07\x00\x00\x00" and buf[4:8] != "\x07\x00\x00\x01": return False
    return (buf[12:16] == "\x06\x00\x00\x00" or buf[12:16] == "\x08\x00\x00\x00")


# Check if a file is a universal library
def is_universal_dylib(path):
    with open(path, "rb") as f:
        buf = f.read(4)

    return (buf == "\xCA\xFE\xBA\xBE")


# Get install name from dylib
def get_install_name(path):
    lines = subprocess.check_output(["otool", "-D", path])
    try:
        line = lines.rstrip().split('\n')[1]
        return [line.strip()]
    except IndexError:
        return []


# Get imports for a Macho file
def get_import_paths(path):
    lines = subprocess.check_output(["otool", "-L", path])

    imports = set()
    for line in lines.rstrip().split('\n')[1:]:
        imports.add(line.split("(", 1)[0].strip())

    for install_name in get_install_name(path):
        imports.remove(install_name)

    return imports


# Fixup imports of destdir:path
def fix_imports(destdir, path, dependency_list, args):
    full_path = os.path.join(destdir, path)

    if path.endswith(".dylib") or path.endswith(".so"):
        if not is_mach_dylib(full_path):
            print("Warning!  " + full_path + " is not a mach dylib file")
            return
    else:
        mode = os.stat(full_path).st_mode
        if not (stat.S_IXUSR & mode): return
        if not is_mach_executable(full_path): return

    if args.verbose:
        print("Fixing imports for %s:" % path)

    for import_path in get_import_paths(full_path):

        if import_path == "/" + path:
            continue

        if import_path.startswith("@rpath"):
            continue

        if import_path.startswith("@loader_path"):
            print("Warning: Import path (%s) starts with loader_path." % import_path)
            continue

        assert import_path[0] == '/'

        # check if the new package depends on its own files, or
        # if the file is provided by one of the dependencies
        test_path = os.path.join(destdir, import_path[1:])
        needs_fixup = os.path.isfile(test_path) or \
                      import_path in dependency_list

        if needs_fixup:
            new_import_path = "@loader_path/%s" % os.path.relpath(import_path, "/%s" % os.path.dirname(path))

            if args.verbose:
                print("%s -> %s" % (import_path, new_import_path))

            subprocess.check_call(["install_name_tool", "-change",
                                   import_path, new_import_path, full_path])

    if args.verbose:
        print("")


# Fixup install_name of destdir:path
def fix_install_name(destdir, path, dependency_list, args):
    full_path = os.path.join(destdir, path)

    if not path.endswith(".dylib") and not path.endswith(".so"):
        return

    assert is_universal_dylib(full_path) or is_universal_dylib(full_path)

    if args.verbose:
        print("Fixing install_name for %s:" % path)

    for install_name in get_install_name(full_path):

        if install_name.startswith("@rpath"):
            continue

        if install_name.startswith("@loader_path"):
            print("Warning: Install name (%s) starts with loader_path." % install_name)
            continue

        if install_name[0] != "/":
            print("Warning: Install name (%s) already a relative path." % install_name)
            continue

        new_install_name = os.path.basename(install_name)

        if args.verbose:
            print("%s -> %s" % (install_name, new_install_name))

        subprocess.check_call(["install_name_tool", "-id", new_install_name, full_path])

    if args.verbose:
        print("")


# Recursively go through all files in DESTDIR, and update import paths
def check_files(destdir, path, dependency_list, args):
    for filename in os.listdir(os.path.join(destdir, path)):
        full_path = os.path.join(destdir, path, filename)

        if os.path.islink(full_path):
            continue

        elif os.path.isfile(full_path):
            if args.install_name:
                fix_install_name(destdir, os.path.join(path, filename), dependency_list, args)
            else:
                fix_imports(destdir, os.path.join(path, filename), dependency_list, args)

        elif os.path.isdir(full_path):
            check_files(destdir, os.path.join(path, filename), dependency_list, args)


def main():
    parser = argparse.ArgumentParser(description="Tool to fixup imports in Macho files")
    parser.add_argument('--filelist', help="List of relative files", default="/dev/null")
    parser.add_argument('--destdir', help="Directory which should be fixed", required=True)
    parser.add_argument('--verbose', action='store_true', help="Print changes")
    parser.add_argument("--install_name", action='store_true', help="Fix install_name instead of imports")
    args = parser.parse_args()

    dependency_list = load_filelist(args.filelist)
    check_files(args.destdir, "", dependency_list, args)


if __name__ == '__main__':
    main()