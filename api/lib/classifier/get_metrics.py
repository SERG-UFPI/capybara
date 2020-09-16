import os
from datetime import datetime
from pathlib import Path

from api import models
from api.lib import utils
from api.lib.test_file_detector import testFileDetector

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


def get_documentation_metric(path):
    _, comment_lines, blank_lines = utils.counter_project(path)

    return (
        (float(comment_lines) / (float(comment_lines) + float(blank_lines)))
        if (comment_lines + blank_lines) != 0
        else 0
    )


def get_tests_metric(path):
    code_source, _, _ = utils.counter_project(path)

    code_test = 0
    all_files = utils.get_list_of_files(path)
    _td = testFileDetector.TestDetector()
    test_files = list(filter(_td.test_search, all_files))
    for file in test_files:
        _code, _, _ = utils.counter_project(file)
        code_test += _code

    return (code_test / code_source) if (code_source) != 0 else 0


def get_community_metric(commits):
    limiar_commits = int(0.8 * len(commits))
    commiters_commits = {}

    for commit in commits:
        author = commit["data"]["author"]
        user = author["name"]
        commiters_commits[user] = commiters_commits.get(user, []) + [commit]

    commiters_commits = {
        k: v
        for k, v in sorted(
            commiters_commits.items(), key=lambda item: len(item[1]), reverse=True
        )
    }

    commiters_len_commits = []
    for key in commiters_commits.keys():
        commiters_len_commits.append(len(commiters_commits[key]))
    aux = 0
    n = 0
    for c in commiters_len_commits:
        aux += c
        n += 1
        if limiar_commits - aux <= 0:
            break

    return n


def retrieve_commits(owner, repository):
    commits = []

    repository_retrieved = models.Repository.objects.get(
        owner=owner, repository=repository
    )
    commits_retrieved = models.Commit.objects.filter(
        repository=repository_retrieved.pk
    ).values("author", "authorDate", "message")

    for commit in commits_retrieved:
        user = commit["author"]
        i = user.find("<")

        name = user[0:i].strip()
        email = user[(i + 1) : (len(user) - 1)]
        updated_on = commit["authorDate"]
        message = commit["message"]

        item = {
            "updated_on": updated_on,
            "data": {"author": {"name": name, "email": email}, "message": message},
        }
        commits.append(item)

    return commits


def retrieve_issues(owner, repository):
    issues = []
    repository_retrieved = models.Repository.objects.get(
        owner=owner, repository=repository
    )
    issues_retrieved = models.Issue.objects.filter(
        repository=repository_retrieved.pk
    ).values()

    for issue in issues_retrieved:
        name = issue["author"]["name"]
        email = issue["author"]["email"]
        updated_on = issue["createdAt"]

        item = {
            "updated_on": updated_on,
            "data": {
                "author": {
                    "name": name,
                    "email": email,
                }
            },
        }

        issues.append(item)

    return issues


def get_metric_history(data):
    if len(data) == 0:
        return 0

    initial_date = data[0]["updated_on"]
    lowest_date = initial_date
    biggest_date = data[0]["updated_on"]
    num_data = len(data)
    for commit in data:
        date = commit["updated_on"]
        if date <= lowest_date:
            lowest_date = date
        elif date >= biggest_date:
            biggest_date = date
    biggest_date = datetime.fromtimestamp(biggest_date)
    lowest_date = datetime.fromtimestamp(lowest_date)
    num_months = (biggest_date.year - lowest_date.year) * 12 + (
        biggest_date.month - lowest_date.month
    )

    return (num_data / num_months) if num_months > 0 else num_data


def get_metric_continuous_integration(path):
    list_ci_files = ["Jenkinsfile", ".travis.yml", ".circleci"]

    files = utils.get_list_of_files(path)

    for file in files:
        for item in list_ci_files:
            if file.find(item) != -1:
                return 1

    return 0


def get_metric_license(path):
    files = utils.get_list_of_files(path)
    for file in files:
        if file.find("LICENSE") != -1:
            return 1
    return 0


def get_all_metrics(owner, repository):
    path = f"{BASE_DIR}/cloned_repositories/{owner}/{repository}/"

    if os.path.exists(path):
        commits = retrieve_commits(owner, repository)
        issues = retrieve_issues(owner, repository)
        documentation_metric = get_documentation_metric(path)
        tests_metric = get_tests_metric(path)
        ci_metric = get_metric_continuous_integration(path)
        license_metric = get_metric_license(path)
        history_commits_metric = get_metric_history(data=commits)
        history_issues_metric = get_metric_history(data=issues)
        community = get_community_metric(commits)

        metrics = {
            "ci": ci_metric,
            "license": license_metric,
            "history": history_commits_metric,
            "management": history_issues_metric,
            "documentation": documentation_metric,
            "community": community,
            "tests": tests_metric,
        }

        return metrics
