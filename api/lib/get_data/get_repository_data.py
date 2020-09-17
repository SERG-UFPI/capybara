import os
import tempfile
from pathlib import Path

import git
from perceval.backends.core.git import Git

from . import get_issues, get_pullrequests, get_repository_info

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Retriever:
    def __init__(self, owner, repository):
        self._owner = owner
        self._repository = repository

    # def start(self):
    #     functions = [
    #         self._get_repository_info,
    #         self._get_commits,
    #         self._get_issues,
    #         self._get_pullrequests,
    #     ]
    #     _threads = [Thread(target=f) for f in functions]

    #     for thread in _threads:
    #         thread.start()

    #     for thread in _threads:
    #         thread.join()

    def get_repository_info(self):
        repository_info = get_repository_info.get_repository_info(
            self._owner, self._repository
        )
        self._clone_repository()

        return repository_info

    def get_commits(self):
        print("==> Retrieving commits...")
        temp_dir = tempfile.TemporaryDirectory(dir=f"{BASE_DIR}")
        repo = Git(
            f"https://github.com/{self._owner}/{self._repository}.git",
            f"{temp_dir.name}/{self._owner}/{self._repository}",
        )
        commits = repo.fetch()
        commits = [item["data"] for item in commits]

        temp_dir.cleanup()
        print("<== Commits retrieved")
        return commits

    def get_issues(self):
        print("==> Retrieving issues...")
        issues = get_issues.get_issues(self._owner, self._repository)
        print("<== Issues retrieved")
        return issues

    def get_pullrequests(self):
        print("==> Retrieving pullrequests...")
        pullrequests = get_pullrequests.get_pullrequests(self._owner, self._repository)
        print("==> PullRequests retrieved")
        return pullrequests

    def _clone_repository(self):
        print("==> Cloning repository...")
        _dir = f"{BASE_DIR}/cloned_repositories/{self._owner}"

        if not os.path.exists(f"{_dir}/{self._repository}"):
            if not os.path.exists(_dir):
                os.makedirs(_dir)

            git.Git(_dir).clone(
                f"https://github.com/{self._owner}/{self._repository}.git"
            )
            print("==> Repository cloned")
