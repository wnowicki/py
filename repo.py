# https://github.com/PyGithub/PyGithub
# $ pip install pygithub

from github import Github
import base64


def get_file_contents(token, repository, file):
    u"""Reads content of file from repository as string """

    g = Github(token.strip())

    return base64.b64decode(g.get_repo(repository).get_file_contents(file).content).decode('utf-8')


if __name__ == "__main__":

    with open('github_token', 'r') as content_file:
        token = content_file.read()

    print(get_file_contents(token, "wnowicki/py", "README.md"))
