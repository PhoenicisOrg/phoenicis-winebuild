import docker
import json


class DockerClient:
    @staticmethod
    def from_env():
        return DockerClient(
            client = docker.from_env(),
            api_client = docker.APIClient()
        )

    def __init__(self, client, api_client):
        self.client = client
        self.api_client = api_client

    def build_image(self, tag, path=".", custom_context=False, fileobj = None, build_args="", dockerfile=""):
        args={"path": path, "tag": tag}
        if custom_context != False:
            args.update({'custom_context': custom_context})
        if build_args != "":
            d = {build_args.split('=',1)[0]: build_args.split('=',1)[1]}
            args.update({'buildargs': d})
        if fileobj is not None:
            args.update({'fileobj': fileobj})
        if dockerfile != "":
            args.update({'dockerfile': dockerfile})

        for line in self.api_client.build(**args):
            for subline in line.decode().split("\r\n"):
                if subline:
                    yield json.loads(subline).get('stream', '')
