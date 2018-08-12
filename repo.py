# https://github.com/PyGithub/PyGithub
# $ pip install pygithub

from github import Github
import base64
import configuration


def get_file_contents(token, repository, file):
    u"""Reads content of file from repository as string """

    g = Github(token.strip())

    return base64.b64decode(g.get_repo(repository).get_file_contents(file).content).decode('utf-8')


if __name__ == "__main__":

    conf = configuration.load()

    print(get_file_contents(conf["github"]["token"], "wnowicki/py", "README.md"))
