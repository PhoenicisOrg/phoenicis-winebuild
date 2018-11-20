import os


class PackageStore:
    @staticmethod
    def get_binaries_path():
        try:
            return os.environ["BINARIES_PATH"]
        except KeyError:
            return os.path.join(os.path.dirname(__file__), "../dist/binaries")

    @staticmethod
    def get_logs_path():
        return os.path.join(os.path.dirname(__file__), "../dist/logs")

    def fetch_distributions(self):
        try:
            return os.listdir(self.get_binaries_path())
        except FileNotFoundError:
            return []

    def fetch_logs(self, distribution):
        try:
            return os.listdir(os.path.join(self.get_logs_path(), distribution))
        except FileNotFoundError:
            return []

    def fetch_binaries(self, distribution):
        return os.listdir(os.path.join(self.get_binaries_path(), distribution))

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

    def fetch_binary_name(self, distribution, binary):
        return os.path.join(PackageStore.get_binaries_path(), distribution, binary)

    def fetch_log_name(self, distribution, log_file):
        return os.path.join(PackageStore.get_logs_path(), distribution, log_file)