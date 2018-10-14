import re

from core.Process import run_and_return

class WineVersionFetcher:
    def fetch_git_tags(self):
        git_tags = run_and_return(["git", "ls-remote", "--tags", "--refs", "git://source.winehq.org/git/wine.git"]).decode("UTF-8")
        return self._parse_tags(git_tags.split("\n")[:-1])

    def fetch_versions(self, majors = None):
        versions = []
        tags = self.fetch_git_tags()
        regex = 'wine-(.+)'

        for tag in tags:
            version_name = tag
            version_number = re.search(regex, tag).group(1)

            versions.append({
                "name": version_name,
                "number": version_number,
                "major": self._fetch_major(version_number)
            })

        if(majors is None):
            return versions
        else:
            return [version for version in versions if version["major"] in majors]

    def _parse_tags(self, tags):
        parsed_tags = []
        regex = '(.+)\\trefs/tags/(.+)'

        for tag in tags:
            parser = re.search(regex, tag)
            parsed_tags.append(parser.group(2))
        return parsed_tags

    def _fetch_major(self, version):
        if('.' not in version):
            return 0
        else:
            return int(version.split('.')[0])
