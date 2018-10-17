import tempfile, tarfile, os

def make_tarfile(content_directory):
    tmp_file = tempfile.NamedTemporaryFile()
    with tarfile.open(tmp_file.name, "w:gz") as tar:
        tar.add(content_directory, arcname=os.path.sep)
    return tmp_file

def make_environment_tarfile():
    environment_dir = os.path.realpath(os.path.dirname(__file__) + "/../environments")
    return make_tarfile(environment_dir)
