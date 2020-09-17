from threading import Thread

from . import commits_parser, issues_parser, pullrequests_parser, repository_parser


class Parser:
    def __init__(self, owner, repository):
        self._owner = owner
        self._repository = repository

    # def start(self):
    #     self.insert_repository()
    #     functions = [self.parse_commits, self.parse_issues, self.parse_pullrequests]
    #     _threads = [Thread(target=f) for f in functions]

    #     for thread in _threads:
    #         thread.start()

    #     for thread in _threads:
    #         thread.join()

    def insert_repository(self, repository_info):
        print("==> Parsing repository...")
        repository_parser.parse_repositorys(repository_info)
        print("<== Repository parsed")

    def parse_commits(self, commits):
        print("==> Parsing commits...")
        commits_parser.parse_commits(self._owner, self._repository, commits)
        print("<== Commits parsed")

    def parse_issues(self, issues):
        print("==> Parsing issues...")
        issues_parser.parse_issues(self._owner, self._repository, issues)
        print("<== Issues parsed")

    def parse_pullrequests(self, pullrequests):
        print("==> Parsing pullrequests...")
        pullrequests_parser.parse_pullrequests(
            self._owner, self._repository, pullrequests
        )
        print("<== PullRequests parsed")
