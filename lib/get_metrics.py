from github import Github, RateLimitExceededException, GithubException
import os
from datetime import datetime
import tempfile
import base64
import subprocess
import json
from id_linking_algorithms.simple_algorithm import start_simple_algorithm
from utils.test_file_detector.testFileDetector import TestDetector

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    for entry in listOfFile:
        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def get_token():
    tokens = []
    index = 1
    while 1:
        token = os.environ.get(f"TOKEN_{index}")
        if token != None:
            tokens.append(token)
            index += 1
        else:
            break
    token_with_greatest_rate_limiting = None
    greatest_rate_limiting = -1
    for token in tokens:
        g_temp = Github(token)
        try:
            rate_limiting = g_temp.rate_limiting[0]
            if rate_limiting != None and rate_limiting > greatest_rate_limiting:
                greatest_rate_limiting = rate_limiting
                token_with_greatest_rate_limiting = token
        except Exception as identifier:
            continue

    return token_with_greatest_rate_limiting


def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    # tags = repository.get_tags()
    # matched_tags = [match for match in tags if match.name == tag]
    # if not matched_tags:
    #     raise ValueError('No Tag or Branch exists with that name')
    # return matched_tags[0].commit.sha


def download_directory(repository, sha, atual_path, server_path="."):
    """
    Download all contents at server_path with commit tag sha in
    the repository.
    """
    contents = repository.get_contents(server_path, ref=sha)
    # contents = repository.get_git_blob(sha=sha)

    for content in contents:
        # print("Processing %s" % content.path)
        if content.type == 'dir':
            download_directory(repository, sha, atual_path, content.path)
        else:
            try:
                path = content.path
                if not os.path.exists(
                        os.path.dirname(atual_path + "/" + path)):
                    try:
                        os.makedirs(os.path.dirname(atual_path + "/" + path))
                    except Exception as e:  # Guard against race condition
                        pass

                file_content = repository.get_contents(path, ref=sha)
                file_data = base64.b64decode(file_content.content)
                file_out = open(atual_path + "/" + path, "w")
                file_out.write(file_data.decode("ISO-8859-1"))
                file_out.close()
            except (Exception, IOError) as exc:
                pass
                # print('Error processing %s: %s', content.path, exc)


def downloadRepo(owner, repository, atual_path):
    token = get_token()
    if token is None:
        return Exception("Espera-se um token de acesso!")
    g = Github(token, timeout=30)
    repo = g.get_repo(f"{owner}/{repository}")
    sha = get_sha_for_tag(repo, "master")
    download_directory(repo, sha, atual_path)


def get_documentation_metric(path):
    cloc_path = f"{path}/../../utils/cloc/cloc"
    process = subprocess.Popen(["perl", cloc_path, path, "--csv"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    stdout, _ = process.communicate()
    stdout = stdout.decode()
    index = stdout.find("SUM")

    content = ["blank", "comment", "code"]
    temp = str(stdout)[index:].replace("\n", "").replace("\'", "").replace(
        "\"", "").split(",")[1:]
    result = dict(zip(content, temp))
    comment_lines = float(result["comment"] if "comment" in result else 0)
    blank_lines = float(result["blank"] if "blank" in result else 0)
    return (comment_lines /
            (comment_lines + blank_lines)) if (comment_lines +
                                               blank_lines) != 0 else 0


def get_tests_metric(path):
    cloc_path = f"{path}/../../utils/cloc/cloc"
    content = ["blank", "comment", "code"]
    parse = lambda string, index: (str(string)[index:].replace(
        "\n", "").replace("\'", "").replace("\"", "").split(",")[1:])
    get_code = lambda x: float(x["code"] if "code" in x else 0)

    process = subprocess.Popen(["perl", cloc_path, path, "--csv"],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

    stdout, _ = process.communicate()
    stdout = stdout.decode()
    index = stdout.find("SUM")
    temp = parse(stdout, index)
    code_source = get_code(dict(zip(content, temp)))
    code_test = 0

    all_files = getListOfFiles(path)
    _td = TestDetector()
    test_files = filter(_td.test_search, all_files)

    for file in test_files:
        process = subprocess.Popen([
            "perl", cloc_path, path, "--match-d=test|spec|tests", "--fullpath",
            "--csv"
        ],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)

        stdout, _ = process.communicate()
        stdout = stdout.decode()
        index = stdout.find("SUM")
        temp = parse(stdout, index)
        code_test += get_code(dict(zip(content, temp)))

    return (code_test / code_source) if (code_source) != 0 else 0


def get_community_metric(commits):
    limiar_commits = int(0.8 * len(commits))
    commiters_commits = {}

    for commit in commits:
        author = commit["data"]["Author"].replace(">", "").split(" <")
        user = author[1]
        commiters_commits[user] = commiters_commits.get(user, []) + [commit]

    commiters_commits = {
        k: v
        for k, v in sorted(commiters_commits.items(),
                           key=lambda item: len(item[1]),
                           reverse=True)
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


def get_metric_history(data):
    if len(data) == 0:
        return 0
    initial_date = datetime.fromtimestamp(data[0]["updated_on"])
    lowest_date = initial_date
    biggest_date = datetime.fromtimestamp(data[0]["updated_on"])
    num_data = len(data)
    for commit in data:
        date = datetime.fromtimestamp(commit["updated_on"])
        if date <= lowest_date:
            lowest_date = date
        elif date >= biggest_date:
            biggest_date = date

    num_months = (biggest_date.year - lowest_date.year) * 12 + (
        biggest_date.month - lowest_date.month)

    return (num_data / num_months) if num_months > 0 else num_data


def get_metric_continuous_integration(owner="", repository=""):
    list_ci_files = ["Jenkinsfile", ".travis.yml", ".circleci"]
    token = get_token()
    if token is None:
        return Exception("Espera-se um token de acesso!")
    g = Github(token)

    repo = g.get_repo(f"{owner}/{repository}")
    content = repo.get_contents("")
    files = [file.path for file in content]
    for ci_file in list_ci_files:
        if ci_file in files:
            return 1
    return 0


def get_metric_license(owner="", repository=""):
    token = get_token()
    if token is None:
        return Exception("Espera-se um token de acesso!")
    g = Github(token)

    repo = g.get_repo(f"{owner}/{repository}")
    content = repo.get_contents("")
    files = [file.path for file in content]
    if "LICENSE" in files:
        return 1
    return 0


def get_all_metrics(owner, repository, issues, commits):
    print(f"Owner: {owner}")
    print(f"Repository: {repository}")
    # print(f"Issues: {issues}")
    # print(f"Commits: {commits}")
    atual_path = tempfile.TemporaryDirectory(dir=BASE_PATH)
    try:
        downloadRepo(owner, repository, atual_path.name)
    except Exception as e:
        pass

    documentation_metric = get_documentation_metric(atual_path.name)
    tests_metric = get_tests_metric(atual_path.name)
    ci_metric = get_metric_continuous_integration(owner=owner,
                                                  repository=repository)
    license_metric = get_metric_license(owner=owner, repository=repository)
    history_commits_metric = get_metric_history(data=commits)
    history_issues_metric = get_metric_history(data=issues)
    community = get_community_metric(commits)

    atual_path.cleanup()

    return {
        "ci": ci_metric,
        "license": license_metric,
        "history": history_commits_metric,
        "management": history_issues_metric,
        "documentation": documentation_metric,
        "community": community,
        "tests": tests_metric
    }


# def main():
#     owner = "ES2-UFPI"
#     repository = "Unichat"
#     # print(get_documentation_metric("./Unichat"))
#     # print(get_tests_metric("./Unichat"))
#     token = get_token()
#     atual_path = tempfile.TemporaryDirectory(dir=BASE_PATH)
#     exception = Exception()
#     while exception != None:
#         try:
#             downloadRepo(owner, repository, atual_path.name, token)
#             exception = None
#         except Exception as e:
#             print(f"Erro download: {e}")

# main()