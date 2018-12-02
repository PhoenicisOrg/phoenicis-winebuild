import docker

from core.DockerClient import DockerClient
from core.LineBuffer import LineBuffer
from core.TarUtils import make_environment_tarfile


class Environment:
    def __init__(self, name: str, os: str, arch: str):
        self.name = name
        self.os = os
        self.arch = arch
        self.with_docker_client(DockerClient.from_env())

    def with_docker_client(self, docker_client):
        self.docker_client = docker_client
        return self

    def full_name(self):
        instance = ":".join([self.os + "-" + self.arch, self.name])
        return "/".join(["phoenicis", "winebuild", instance])

    def dockerfile_name(self):
        return "-".join([self.os, self.arch, self.name])

    def get(self):
        return self.docker_client.client.images.get(self.full_name())

    def state(self):
        try:
            self.get()
            return "READY"
        except docker.errors.ImageNotFound:
            return "NOT_READY"

    def build(self, callback = None):
        buffer = LineBuffer()
        for x in self.docker_client.build_image(
            path = ".",
            custom_context = True,
            fileobj = make_environment_tarfile(),
            dockerfile = self.dockerfile_name(),
            tag = self.full_name()
        ):
            if(callback is None):
                callback = lambda content: print(content, end='')

            self.callback_line_by_line(buffer, x, callback)

    def callback_line_by_line(self, buffer, data_written, callback):
        buffer.append(data_written)
        if(not buffer.empty()):
            for line in buffer.get():
                callback(line)

    def clean(self):
        try:
            self.docker_client.client.images.remove(
                image = self.full_name(),
                force = True
            )
        except docker.errors.NotFound:
            pass
