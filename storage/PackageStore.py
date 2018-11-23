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

    def fetch_distributions(self):
        try:
            return os.listdir(self.get_binaries_path())
        except FileNotFoundError:
            return []

    def fetch_missing_versions(self, distribution):
        all_wine_versions = WineVersionFetcher().fetch_versions(majors=[2, 3]) # FIXME: Put inside a configuration file
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
                match = re.search(r"phoenicis-(.+)-"+distribution+".log", log)
                if match is not None:
                    version_number = match.group(1)
                    versions.add(version_number)

            binaries = os.listdir(os.path.join(self.get_binaries_path(), distribution))
            for binary in binaries:
                match = re.search(r"phoenicis-(.+)-"+distribution+".tar.gz", binary)
                if match is not None:
                    version_number = match.group(1)
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
        binary = "phoenicis-%s-%s.tar.gz" % (version, distribution)
        binary_path = os.path.join(PackageStore.get_binaries_path(), distribution, binary)
        if os.path.exists(binary_path):
            return binary_path
        else:
            return None

    def fetch_log_name(self, distribution, version):
        log_name = "phoenicis-%s-%s.log" % (version, distribution)
        log_path = os.path.join(PackageStore.get_logs_path(), distribution, log_name)

        if os.path.exists(log_path):
            return log_path
        else:
            return None