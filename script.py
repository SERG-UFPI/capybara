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
from git_retriever.retriever import GithubRetriever
from id_linking_algorithms.simple_algorithm import start_simple_algorithm
from id_linking_algorithms.bird_algorithm import start_bird_algorithm

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
DB_CONNECTION = os.environ.get("DB_CONNECTION")


def _insertMapIdentification(map_identification, algorithm, owner, repository, connection):
    cursor = connection.cursor()
    # print(map_identification)
    for i in map_identification:
        for value in list(i.values())[0]:
            id_value = int(list(i.keys())[0])
            sql = """
                INSERT INTO
                    map_identification (id, id_identification, algorithm, owner, repository)
                VALUES
                    (%s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING;
            """

            cursor.execute(
                sql, (id_value, value["id"], algorithm, owner, repository))
            connection.commit()


def linkIds(user_owner, repo_name, algo):
    if algo.lower() != "simple" and algo.lower() != "bird":
        print(algo)
        return {"error": "Algorithm does not exist"}

    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_identification (
            id BIGSERIAL,
            owner TEXT,
            repository TEXT,
            id_identification INTEGER REFERENCES identification(id),
            algorithm TEXT NOT NULL,
            PRIMARY KEY (id, owner, repository, id_identification, algorithm)
        );
    """)

    sql_result = f"""SELECT
            map_identification.id, identification.name, identification.email, map_identification.algorithm
        FROM
            identification, map_identification
        WHERE
            identification.owner = \'{user_owner}\' AND
            identification.repository = \'{repo_name}\' AND
            identification.id = map_identification.id_identification AND
            map_identification.algorithm=\'{algo.upper()}\'
        ;"""

    cursor.execute(sql_result)
    tables = cursor.fetchall()

    # print(f"Resultado busca 1: {tables}")
    # print(type(tables))

    map_identification = []

    if tables != None and len(tables) > 0:
        # print("Entrou")
        for t in tables:
            item = {
                "id": t[0],
                "name": t[1],
                "email": t[2],
                "algorithm": t[3]
            }
            map_identification.append(item)

        # print(map_identification)
        conn.close()
        return {"map_identification": map_identification}

    sql = f"""SELECT
            id, name, email
        FROM
            identification
        WHERE
            identification.owner = \'{user_owner}\' AND
            identification.repository = \'{repo_name}\'
        ;"""

    cursor.execute(sql)
    tables = cursor.fetchall()

    users = []
    for user in tables:
        users.append(
            {
                "id": user[0],
                "name": user[1],
                "email": user[2]
            }
        )
    # print(users)

    result = None

    if algo.lower() == "simple":
        result = start_simple_algorithm(users=users)
        # print(result)
        _insertMapIdentification(result, "SIMPLE", user_owner, repo_name, conn)
    else:
        result = start_bird_algorithm(users=users)
        # print(result)
        _insertMapIdentification(result, "BIRD", user_owner, repo_name, conn)

    # print(f"Resultado: {result}")

    # print(sql_result)

    cursor.execute(sql_result)
    tables = cursor.fetchall()

    # print(f"Resultado busca 2: {tables}")

    map_identification = []

    if tables != None and len(tables) > 0:
        for t in tables:
            item = {
                "id": t[0],
                "name": t[1],
                "email": t[2],
                "algorithm": t[3]
            }
            map_identification.append(item)

        # print(map_identification)
        conn.close()
        return {"map_identification": map_identification}
    conn.close()


def getCommits(user_owner, repo_name):
    with tempfile.TemporaryDirectory(dir=BASE_PATH) as atual_path:
        repo = Git(f"https://github.com/{user_owner}/{repo_name}.git",
                   f"{atual_path}/{user_owner}_{repo_name}.git")
        commits = repo.fetch()
    return commits


def getIssues(user_owner, repo_name, tokens):
    gr = GithubRetriever(tokens=tokens)
    issues = gr.retrieve_issues(owner=user_owner, repository=repo_name)
    return issues


def getPRs(user_owner, repo_name, tokens):
    gr = GithubRetriever(tokens=tokens)
    prs = gr.retrieve_pullrequests(owner=user_owner, repository=repo_name)
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
    sql = f"""SELECT (owner, repository) FROM repositorys;"""

    cursor.execute(sql)
    tables = cursor.fetchall()

    for repository in tables:
        repo = repository[0].replace("(", "").replace(")", "").split(",")
        if repo[0] == user_owner and repo[1] == repo_name:
            return True

    return False


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

    owner_avatar_url = repo.owner.avatar_url
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
    size = repo.size

    # A linguagem com o maior número de linhas de código será a main_language
    aux = repo.get_languages()
    aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}
    main_language = list(aux.keys())[-1]

    contents_aux = repo.get_contents(".")
    def contents_func(x): return repo.get_contents(x)

    num_files = getNumFiles(user_owner, repo_name)

    yield {
        'owner_avatar_url': owner_avatar_url,
        'owner': user_owner,
        'repository': repo_name,
        # 'num_authors': num_authors,
        'has_wiki': has_wiki,
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


def returnIssues(owner, repository, limit, pr_as_issue):
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True
    # conn = psycopg2.connect(data_base_url)
    conn.autocommit = True
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
        repository_issues.id_issue = issues.id 
    LIMIT {"null" if limit == 0 else limit};
    """
    # {"" if pr_as_issue else "AND issues.pull_request IS NULL"}
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
    return len(result), result


def returnCommits(owner, repository, limit):
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True

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
    return len(result), result


def returnPullRequests(owner, repository, limit):
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True

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
    return len(result), result


def returnRepositorys():
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True

    cursor = conn.cursor()

    rows_to_fecth = "owner, repository, owner_avatar_url, description, language"

    sql = f"""
    SELECT
        {rows_to_fecth}
    FROM
        repositorys;
    """
    lines = []
    try:
        cursor.execute(sql)
        lines = cursor.fetchall()
    except Exception:
        pass

    result = []
    print(lines)
    for line in lines:
        temp = {}
        temp["owner"] = line[0]
        temp["repository"] = line[1]
        temp["owner_avatar_url"] = line[2]
        temp["description"] = line[3]
        temp["language"] = line[4]
        result.append(temp)

    cursor.close()
    conn.close()
    return result


def returnRepository(owner, repository):
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True

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
    conn = psycopg2.connect(DB_CONNECTION)
    conn.autocommit = True

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

    tables = getColumnsTable(cursor)

    try:
        repository_exists = checkRepoExists(owner, repository_name, cursor)
    except Exception:
        pass
    repository_exists = False

    if repository_exists is None or not repository_exists:
        print("GETING DATA...")

        commits = {}
        issues = {}
        pullrequests = {}

        repository_info = list(generateRepository(owner, repository_name))
        print(repository_info)
        print("RETRIEVING COMMITS...")
        commits = [item["data"] for item in getCommits(owner, repository_name)]
        print("COMMITS RETRIEVED")

        print("RETRIEVING ISSUES...")
        issues = getIssues(owner, repository_name, tokens)
        # issues = []
        # issues = [item for item in temp if not ("pull_request" in item["data"].keys())]
        print("ISSUES RETRIEVED")

        print("RETRIEVING PULL_REQUESTS...")
        pullrequests = getPRs(owner, repository_name, tokens)
        # pullrequests = []
        print("PULL_REQUESTS RETRIEVED")

        repository = {
            "repository": repository_info,
            "commits": commits,
            "issues": issues,
            "pullrequests": pullrequests
        }
        print("DATA FETCHED!")

        tables = None
        try:
            tables = getColumnsTable(cursor)
        except Exception:
            tables = []
        # print(tables)
        jsonToSql(conn, tables, repository)

    conn.close()


if __name__ == "__main__":
    # run("d3", "d3")
    # run("Mex978", "compilador")
    # run("ES2-UFPI", "Unichat")
    # get_all_metrics("ES2-UFPI", "Unichat")
    a = linkIds("ES2-UFPI", "Unichat", "simple")
    print(a)
    # run("gatsbyjs", "gatsby")
