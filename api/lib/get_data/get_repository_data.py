import os
import tempfile
from pathlib import Path
from threading import Thread

import git
from perceval.backends.core.git import Git

from . import get_issues, get_pullrequests, get_repository_info

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Retriever:
    def __init__(self, owner, repository):
        self._owner = owner
        self._repository = repository

    repository_info = None
    commits = None
    issues = None
    pullrequests = None

    def start(self):
        functions = [
            self._get_repository_info,
            self._get_commits,
            self._get_issues,
            self._get_pullrequests,
        ]
        _threads = [Thread(target=f) for f in functions]

        for thread in _threads:
            thread.start()

        for thread in _threads:
            thread.join()

    def _get_repository_info(self):
        print("===> Retrieving repository data...")
        self._clone_repository()

        self.repository_info = get_repository_info.getRepositoryInfo(
            self._owner, self._repository
        )

        print("<== Repository data retrieved")

    def _get_commits(self):
        print("===> Retrieving commits...")
        temp_dir = tempfile.TemporaryDirectory(dir=f"{BASE_DIR}")

        try:
            repo = Git(
                f"https://github.com/{self._owner}/{self._repository}.git",
                f"{temp_dir.name}/{self._owner}/{self._repository}",
            )
            self.commits = repo.fetch()
            self.commits = [item["data"] for item in self.commits]
        finally:
            temp_dir.cleanup()
            print("<== Commits retrieved")

    def _get_issues(self):
        print("===> Retrieving issues...")
        self.issues = get_issues.get_issues(self._owner, self._repository)
        print("<== Issues retrieved")

    def _get_pullrequests(self):
        print("===> Retrieving pullrequests...")
        self.pullrequests = get_pullrequests.get_pullrequests(
            self._owner, self._repository
        )
        print("<== Pullrequests retrieved")

    def _clone_repository(self):
        _dir = f"{BASE_DIR}/cloned_repositories/{self._owner}/{self._repository}"

        if not os.path.exists(_dir):
            print("===> Cloning repository...")
            try:
                if not os.path.exists(_dir):
                    os.makedirs(_dir)

                git.Git(_dir).clone(
                    f"https://github.com/{self._owner}/{self._repository}.git"
                )
                print("<== Repository cloned")
            except Exception as error:
                print(f"Error on clone repository: {error}")
