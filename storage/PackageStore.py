import os, re

from wine.WineVersionFetcher import WineVersionFetcher

class PackageStore:
    @staticmethod
    def get_binaries_path():
        try:
            return os.environ["BINARIES_PATH"]
        except KeyError:
            return os.path.join(os.path.dirname(__file__), "../dist/binaries")

    @staticmethod
    def get_logs_path():
        try:
            return os.environ["LOGS_PATH"]
        except KeyError:
            return os.path.join(os.path.dirname(__file__), "../dist/logs")

    @staticmethod
    def get_runtimes_path():
        try:
            return os.environ["RUNTIME_PATH"]
        except KeyError:
            return os.path.join(os.path.dirname(__file__), "../dist/runtimes")


    def fetch_distributions(self):
        try:
            return os.listdir(self.get_binaries_path())
        except FileNotFoundError:
            return []

    def fetch_missing_versions(self, distribution):
        # FIXME: The right distribution data should be passed instead of concatenating / parsing
<<<<<<< HEAD
        all_wine_versions = WineVersionFetcher(distribution.split("-")[0]).fetch_versions(majors=[2, 3, 4, 5, 6, 7, 8]) # FIXME: Put inside a configuration file
=======
        all_wine_versions = WineVersionFetcher(distribution.split("-")[0]).fetch_versions(majors=[2, 3, 4, 5, 6, 7, 8, 9]) # FIXME: Put inside a configuration file
>>>>>>> 3b409a4892875922bc993ca8d2f9cf9d13bbc649

        built_versions = self.fetch_versions(distribution)
        missing_versions = []
        for version in all_wine_versions:
            if version["name"] not in built_versions:
                missing_versions += [version["name"]]

        return missing_versions

    def fetch_versions(self, distribution):
        versions = set()
        try:
            logs = os.listdir(os.path.join(self.get_logs_path(), distribution))
            for log in logs:
                match = re.search(r"(phoenicis|PlayOnLinux)-(.+)-"+distribution+".log", log)
                if match is not None:
                    version_number = match.group(2)
                    versions.add(version_number)

            binaries = os.listdir(os.path.join(self.get_binaries_path(), distribution))
            for binary in binaries:
                match = re.search(r"(phoenicis|PlayOnLinux)-(.+)-"+distribution+".tar.gz", binary)
                if match is not None:
                    version_number = match.group(2)
                    versions.add(version_number)

            return list(versions)
        except FileNotFoundError:
            return []

    class fetch_log():
        def __init__(self, distribution, log):
            self.file_name = os.path.join(PackageStore.get_logs_path(), distribution, log)

        def __enter__(self):
            self.file = open(self.file_name, 'rb')
            return self.file

        def __exit__(self, type, value, traceback):
            self.file.close()

    class fetch_binary():
        def __init__(self, distribution, binary):
            self.file_name = os.path.join(PackageStore.get_binaries_path(), distribution, binary)

        def __enter__(self):
            self.file = open(self.file_name, 'rb')
            return self.file

        def __exit__(self, type, value, traceback):
            self.file.close()

    def fetch_binary_name(self, distribution, version):
        binary = "PlayOnLinux-%s-%s.tar.gz" % (version, distribution)
        binary_path = os.path.join(PackageStore.get_binaries_path(), distribution, binary)
        if os.path.exists(binary_path):
            return binary_path
        else:
            return None

    def fetch_log_name(self, distribution, version):
        log_name = "PlayOnLinux-%s-%s.log" % (version, distribution)
        log_path = os.path.join(PackageStore.get_logs_path(), distribution, log_name)

        if os.path.exists(log_path):
            return log_path
        else:
            return None