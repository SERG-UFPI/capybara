from . import repository_parser, commits_parser, issues_parser, pullrequests_parser
from threading import Thread


class Parser:
    def __init__(self, owner, repository, repository_info, commits, issues, pullrequests):
        self._owner = owner
        self._repository = repository
        self.repository_info = repository_info
        self.commits = commits
        self.issues = issues
        self.pullrequests = pullrequests

    def start(self):
        self.insert_repository()
        functions = [self.parse_commits,
                     self.parse_issues, self.parse_pullrequests]
        _threads = [Thread(target=f) for f in functions]

        for t in _threads:
            t.start()

        for t in _threads:
            t.join()

    def insert_repository(self):
        print('==> Parsing repository...')
        try:
            repository_parser.parseRepositorys(self.repository_info)
        except Exception as e:
            print(f'Error on parse repository: {e}')
        print('<== Repository parsed')

    def parse_commits(self):
        print('==> Parsing commits...')
        commits_parser.parseCommits(
            self._owner, self._repository, self.commits)
        print('<== Commits parsed')

    def parse_issues(self):
        print('==> Parsing issues...')
        issues_parser.parseIssues(
            self._owner, self._repository, self.issues)
        print('<== Issues parsed')

    def parse_pullrequests(self):
        print('==> Parsing pullrequests...')
        pullrequests_parser.parsePullRequests(
            self._owner, self._repository, self.pullrequests)
        print('<== PullRequests parsed')
