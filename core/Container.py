import docker, io, tarfile, os, tempfile

from core.DockerClient import DockerClient
from core.Process import run
from core.TarUtils import make_tarfile
from core.LineBuffer import LineBuffer

class Container:
    @staticmethod
    def from_id(container_id):
        container = Container(None)
        container.container = container.docker_client.client.containers.get(container_id)
        return container

    def __init__(self, environment):
        self.container = None
        self.environment = environment
        self._logfile = None
        self._output_callback = lambda line: print(line, end = '')
        self.with_docker_client(DockerClient.from_env())

    def with_output_callback(self, output_callback):
        self._output_callback = output_callback
        return self

    def with_docker_client(self, docker_client):
        self.docker_client = docker_client
        return self

    def with_log_file(self, logfile):
        self._logfile = logfile
        return self

    def start(self):
        self.container = self.docker_client.client.containers.run(self.environment.full_name(), detach = True, stdin_open = True, tty = True)

    def run(self, command, workdir = None):
        buffer = LineBuffer()

        if self._logfile is not None:
            logfile = open(self._logfile, 'w')
        else:
            logfile = None

        def do_output(chunk):
            if self._output_callback is not None:
                buffer.append(chunk)
                if(not buffer.empty()):
                    for line in buffer.get():
                        self._output_callback(line)

            if logfile is not None:
                logfile.write(chunk)
                logfile.flush()

        try:
            if(workdir is None):
                execution = self.container.exec_run(command, stdout = True, stderr = True, stream = True, privileged = True)
            else:
                execution = self.container.exec_run(command, stdout = True, stderr = True, workdir = workdir, stream = True)

            for response in execution:
                if response is not None:
                    for chunk in response:
                        do_output(chunk.decode())
        finally:
            if(logfile is not None):
                logfile.close()

    def put_directory(self, local_directory, remote_directory):
        tar_file = make_tarfile(local_directory)
        self.run(["mkdir", "-p", remote_directory])
        self.put_file(tar_file.name, remote_directory, remote_file_name = "temp.tar.gz")
        self.run(["tar", "xvf", "temp.tar.gz"], workdir = remote_directory)
        self.run(["rm", "temp.tar.gz"], workdir = remote_directory)

    def put_file(self, local_file, remote_directory, remote_file_name = None):
        if(remote_file_name is None):
            remote_file_name = os.path.basename(local_file)

        tarstream = io.BytesIO()
        with tarfile.open(fileobj=tarstream, mode='w') as tarfile_:
            with open(local_file, mode = 'rb') as scriptfile:
                encoded_file_contents = scriptfile.read()
                tarinfo = tarfile.TarInfo(remote_file_name)
                tarinfo.size = len(encoded_file_contents)
                tarfile_.addfile(tarinfo, io.BytesIO(encoded_file_contents))

        tarstream.seek(0)
        self.docker_client.api_client.put_archive(
            container = self.container.id,
            path = remote_directory,
            data = tarstream
        )

    def get_file(self, file, local_file):
        if(local_file is None):
            local_file = "archive.tar.gz"

        strm, stat = self.docker_client.api_client.get_archive(self.container.id, file)
        with open(local_file, mode = 'wb') as outfile:
            for d in strm:
                outfile.write(d)

    def run_script(self, script):
        self.put_file(script, "/tmp/", "script")
        self.run(["bash", "/tmp/script"])

    def clean(self):
        self.container.kill()
        self.container.remove()
