'''
@Author: Max Nícolas de Oliveira Lima

'''
import psycopg2
import json
import os
from lib.json_to_sql import jsonToSql
from perceval.backends.core.github import GitHub
from perceval.backends.core.git import Git
from lib.get_metrics import get_all_metrics, get_community_metric
from utils.get_token import get_token
import lib.classifiers as cassifier
from github import Github
import tempfile

BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def getCommits(user_owner, repo_name):
    with tempfile.TemporaryDirectory(dir=BASE_PATH) as atual_path:
        repo = Git(f"https://github.com/{user_owner}/{repo_name}.git",
                   f"{atual_path}/{user_owner}_{repo_name}.git")
        commits = repo.fetch()
        return commits


def getIssues(user_owner, repo_name, tokens):
    repo = GitHub(owner=user_owner,
                  repository=repo_name,
                  api_token=tokens,
                  sleep_for_rate=True)
    issues = repo.fetch(category="issue")
    return issues


def getPRs(user_owner, repo_name, tokens):
    repo = GitHub(owner=user_owner,
                  repository=repo_name,
                  api_token=tokens,
                  sleep_for_rate=True)
    prs = repo.fetch(category="pull_request")
    return prs


def getColumnsTable(cursor):
    cursor.execute("""SELECT *
               FROM information_schema.columns
               WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
               ORDER BY table_schema, table_name""")
    tables = {}
    for row in cursor:
        table = row[2]
        column = row[3]
        type_column = row[7]

        if table in tables:
            tables[table].append({"name": row[3], "type": row[7]})
        else:
            tables[table] = [{"name": row[3], "type": row[7]}]

    return tables


def checkRepoExists(user_owner, repo_name, cursor):
    sql = f"""
        SELECT EXISTS (
            SELECT *
            FROM   information_schema.tables
            WHERE  table_schema = 'serg'
            AND    table_name = 'repositorys'
        );
    """

    cursor.execute(sql)
    tables = cursor.fetchall()

    if tables[0][0]:
        sql = f"""
        SELECT
            *
        FROM
            repositorys
        WHERE
            owner = {user_owner} AND
            repository = {repo_name}
        ;"""
        cursor.execute(sql)
        return cursor.fetchall()
    return None

numFiles = 0

def getNumFilesAux(repo, dir):
    global numFiles
    contents = repo.get_contents(dir)

    for content in contents:
        if content.type == 'dir':
            getNumFilesAux(repo, content.path)
        else:
            numFiles += 1



def getNumFiles(user_owner, repo_name):
    global numFiles
    token = get_token()
    g = Github(token)
    repo = g.get_repo(f'{user_owner}/{repo_name}')
    numFiles = 0
    getNumFilesAux(repo, dir=".")
    return numFiles

def generateRepository(user_owner, repo_name):
    token = get_token()
    g = Github(token)
    repo = g.get_repo(f'{user_owner}/{repo_name}')
    
    COMMITS = repo.get_commits()

    fullname = repo.full_name
    clone_url = repo.clone_url
    created_at = repo.created_at.timestamp()
    default_branch = repo.default_branch
    description = repo.description
    fork = repo.fork
    forks_count = repo.forks_count
    homepage = repo.homepage
    language = repo.language
    name = repo.name
    open_issues = repo.open_issues
    pushed_at = repo.pushed_at.timestamp()
    archived = repo.archived
    stargazers_count = repo.stargazers_count
    updated_at = repo.updated_at.timestamp()
    watchers_count = repo.watchers_count
    has_wiki = repo.has_wiki
    # num_authors = repo.get_collaborators().totalCount
    subscribers_count = repo.subscribers_count
    commits_count = COMMITS.totalCount
    last_commit = COMMITS[0]
    size = repo.size
    
    # A linguagem com o maior número de linhas de código será a main_language
    aux = repo.get_languages()
    aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}
    main_language = list(aux.keys())[-1]

    contents_aux = repo.get_contents(".")
    contents_func = lambda x: repo.get_contents(x)

    num_files = getNumFiles(user_owner, repo_name)


    yield {
        'data': {
            'owner': user_owner, 
            'repository': repo_name,
            # 'num_authors': num_authors,
            'fullname': fullname,
            'clone_url': clone_url,
            'created_at': created_at,
            'default_branch': default_branch,
            'description': description,
            'fork': fork,
            'forks_count': forks_count,
            'homepage': homepage,
            'language': language,
            'main_language': main_language,
            'name': name,
            'open_issues': open_issues,
            'pushed_at': pushed_at,
            'stargazers_count': stargazers_count,
            'updated_at': updated_at,
            'watchers_count': watchers_count,
            'subscribers_count': subscribers_count,
            'archived': archived,
            'num_files': num_files,
            'size': size
        }
    }


def returnIssues(owner, repository, limit, pr_as_issue):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)
    # conn = psycopg2.connect(data_base_url)
    cursor = conn.cursor()

    tables = getColumnsTable(cursor)

    columns = [atrib["name"] for atrib in tables["issues"]]

    rows_to_fecth = ""

    for column in columns:
        if column == columns[-1]:
            rows_to_fecth += f"issues.{column}"
        else:
            rows_to_fecth += f"issues.{column}, "

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        issues,
        repository_issues
    WHERE
        repository_issues.owner = %s AND
        repository_issues.repository = %s AND
        repository_issues.id_issue = issues.id {"" if pr_as_issue else "AND issues.pull_request IS NULL"}
    LIMIT {"null" if limit == 0 else limit};
    """
    cursor.execute(sql, (owner, repository))
    lines = cursor.fetchall()

    result = []

    for line in lines:
        temp = {}

        for i in range(len(line)):
            temp[columns[i]] = line[i]
        result.append(temp)

    cursor.close()
    conn.close()
    return result


def returnCommits(owner, repository, limit):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)

    cursor = conn.cursor()

    tables = getColumnsTable(cursor)

    columns = [atrib["name"] for atrib in tables["commits"]]

    rows_to_fecth = ""

    for column in columns:
        if column == columns[-1]:
            rows_to_fecth += f"commits.{column}"
        else:
            rows_to_fecth += f"commits.{column}, "

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        commits,
        repository_commits
    WHERE
        repository_commits.owner = %s AND
        repository_commits.repository = %s AND
        repository_commits.commit = commits.commit
    LIMIT {"null" if limit == 0 else limit};
    """
    cursor.execute(sql, (owner, repository))
    lines = cursor.fetchall()

    result = []

    for line in lines:
        temp = {}

        for i in range(len(line)):
            temp[columns[i]] = line[i]
        result.append(temp)

    cursor.close()
    conn.close()
    return result


def returnPullRequests(owner, repository, limit):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)

    cursor = conn.cursor()

    tables = getColumnsTable(cursor)

    columns = [atrib["name"] for atrib in tables["pullrequests"]]

    rows_to_fecth = ""

    for column in columns:
        if column == columns[-1]:
            rows_to_fecth += f"pullrequests.{column}"
        else:
            rows_to_fecth += f"pullrequests.{column}, "

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        pullrequests,
        repository_pullrequests
    WHERE
        repository_pullrequests.owner = %s AND
        repository_pullrequests.repository = %s AND
        repository_pullrequests.id_pull_request = pullrequests.id
    LIMIT {"null" if limit == 0 else limit};
    """
    cursor.execute(sql, (owner, repository))
    lines = cursor.fetchall()

    result = []

    for line in lines:
        temp = {}

        for i in range(len(line)):
            temp[columns[i]] = line[i]
        result.append(temp)

    cursor.close()
    conn.close()
    return result

def returnRepositorys():
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)

    cursor = conn.cursor()

    rows_to_fecth = "owner, repository"

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        repositorys;
    """
    cursor.execute(sql)
    lines = cursor.fetchall()

    result = []

    for line in lines:
        temp = {}
        temp["owner"] = line[0]
        temp["repository"] = line[1]
        result.append(temp)

    cursor.close()
    conn.close()
    return result

def returnRepository(owner, repository):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)

    cursor = conn.cursor()

    tables = getColumnsTable(cursor)

    columns = [atrib["name"] for atrib in tables["repositorys"]]

    rows_to_fecth = ""

    for column in columns:
        if column == columns[-1]:
            rows_to_fecth += f"repositorys.{column}"
        else:
            rows_to_fecth += f"repositorys.{column}, "

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        repositorys
    WHERE
        repositorys.owner = %s AND
        repositorys.repository = %s;
    """
    cursor.execute(sql, (owner, repository))
    lines = cursor.fetchall()

    result = {}

    for i in range(len(lines[0])):
        result[columns[i]] = lines[0][i]

    cursor.close()
    conn.close()
    return result


def run(owner, repository_name):
    conn = psycopg2.connect(database="postgres",
                            user="postgres",
                            password="maxlima13",
                            port=5432)

    cursor = conn.cursor()

    tokens = []

    index = 1

    while 1:
        token = os.environ.get(f"TOKEN_{index}")
        if token != None:
            tokens.append(token)
            index += 1
        else:
            break

    repositorys = checkRepoExists(owner, repository_name, cursor)

    if repositorys is None:
        print("GETING DATA...")

        commits = {}
        issues = {}
        pullrequests = {}

        repository_info = list(generateRepository(owner, repository_name))
        print(repository_info)
        print("RETRIEVING COMMITS...")
        commits = list(getCommits(owner, repository_name))
        print("COMMITS RETRIEVED")

        print("RETRIEVING ISSUES...")
        issues = list(getIssues(owner, repository_name, tokens))
        # issues = [item for item in temp if not ("pull_request" in item["data"].keys())]
        print("ISSUES RETRIEVED")

        # return True

        # metrics = get_all_metrics(owner, repository_name, issues, commits)

        # if (not cassifier.run(metrics)):
        #     raise Exception(
        #         "O repositório não possui indícios suficientes de engenharia de software"
        #     )

        print("RETRIEVING PULL_REQUESTS...")
        pullrequests = list(getPRs(owner, repository_name, tokens))
        print("PULL_REQUESTS RETRIEVED")

        repository = {
            "repository": repository_info,
            "commits": commits,
            "issues": issues,
            "pullrequests": pullrequests
        }
        print("DATA FETCHED!")

        tables = getColumnsTable(cursor)
        jsonToSql(conn, tables, repository)

    conn.close()


if __name__ == "__main__":
    # run("Mex978", "compilador")
    # run("ES2-UFPI", "Unichat")
    run("gatsbyjs", "gatsby")
