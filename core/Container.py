import io
import os
import tarfile

from core.DockerClient import DockerClient
from core.LineBuffer import LineBuffer
from core.TarUtils import make_tarfile


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
        self._output_callback = lambda line: print(line, end='')
        self.containerEnvironmentVariables = {}
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
        self.container = self.docker_client.client.containers.run(self.environment.full_name(), detach=True,
                                                                  stdin_open=True, tty=True)

    def env(self, key, value):
        self.containerEnvironmentVariables[key] = value

    def run(self, command, workdir=None):
        buffer = LineBuffer()

        if self._logfile is not None:
            logfile = open(self._logfile, 'a')
        else:
            logfile = None

        def do_output(chunk):
            if self._output_callback is not None:
                buffer.append(chunk)
                if not buffer.empty():
                    for line in buffer.get():
                        if line.startswith("[THROW] "):
                            raise Exception("Builder threw an exception: " + line)
                        self._output_callback(line)

            if logfile is not None:
                logfile.write(chunk)
                logfile.flush()

        try:
            resp = self.docker_client.api_client.exec_create(
                self.container.id,
                command,
                stdout=True,
                stderr=True,
                stdin=False,
                tty=False,
                privileged=True,
                user='',
                environment=self.containerEnvironmentVariables,
                workdir=workdir
            )
            exec_output = self.docker_client.api_client.exec_start(
                resp['Id'], detach=False, tty=False, stream=True, socket=False
            )

            for chunk in exec_output:
                do_output(chunk.decode())

            exit_code = self.docker_client.api_client.exec_inspect(resp['Id'])['ExitCode']
            if exit_code != 0 and exit_code is not None:
                raise Exception("Builder returned a non-zero code: " + str(exit_code))

        finally:
            if logfile is not None:
                logfile.close()

    def put_directory(self, local_directory, remote_directory):
        tar_file = make_tarfile(local_directory)
        self.run(["mkdir", "-p", remote_directory])
        self.put_file(tar_file.name, remote_directory, remote_file_name="temp.tar.gz")
        self.run(["tar", "xvf", "temp.tar.gz"], workdir=remote_directory)
        self.run(["rm", "temp.tar.gz"], workdir=remote_directory)

    def put_file(self, local_file, remote_directory, remote_file_name=None):
        if remote_file_name is None:
            remote_file_name = os.path.basename(local_file)

        tarstream = io.BytesIO()
        with tarfile.open(fileobj=tarstream, mode='w') as tarfile_:
            with open(local_file, mode='rb') as scriptfile:
                encoded_file_contents = scriptfile.read()
                tarinfo = tarfile.TarInfo(remote_file_name)
                tarinfo.size = len(encoded_file_contents)
                tarfile_.addfile(tarinfo, io.BytesIO(encoded_file_contents))

        tarstream.seek(0)
        self.docker_client.api_client.put_archive(
            container=self.container.id,
            path=remote_directory,
            data=tarstream
        )

    def get_file(self, file, local_file):
        if (local_file is None):
            local_file = "archive.tar.gz"

        strm, stat = self.docker_client.api_client.get_archive(self.container.id, file)
        with open(local_file, mode='wb') as outfile:
            for d in strm:
                outfile.write(d)

    def run_script(self, script):
        self.put_file(script, "/tmp/", "script")
        self.run(["bash", "/tmp/script"])

    def clean(self):
        self.container.kill()
        self.container.remove()
