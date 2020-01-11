'''
@Author: Max Nícolas de Oliveira Lima

'''
import psycopg2
import json
import os
from lib.json_to_sql import jsonToSql
from perceval.backends.core.github import GitHub
from perceval.backends.core.git import Git


def getCommits(user_owner, repo_name):
    repo = Git(f"https://github.com/{user_owner}/{repo_name}.git",
               f"https://github.com/{user_owner}/{repo_name}.git")
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


def generateRepository(user_owner, repo_name):
    yield {'data': {'owner': user_owner, 'repository': repo_name}}


def returnIssues(owner, repository, limit):
    data_base_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(data_base_url, sslmode='require')
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
        repository_issues.id_issue = issues.id
    LIMIT {"null" if limit is None else limit};
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
    data_base_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(data_base_url, sslmode='require')
    # conn = psycopg2.connect(data_base_url)
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
    LIMIT {"null" if limit is None else limit};
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


def run(owner, repository):
    data_base_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(data_base_url, sslmode='require')
    # conn = psycopg2.connect(data_base_url)

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

    repositorys = checkRepoExists(owner, repository, cursor)

    if repositorys is None:
        print("GETING DATA...")

        commits = {}
        issues = {}
        pullrequests = {}

        repository_info = list(generateRepository(owner, repository))
        print("RETRIEVING COMMITS...")
        commits = list(getCommits(owner, repository))
        print(commits)
        print("COMMITS RETRIEVED")

        print("RETRIEVING ISSUES...")
        issues = list(getIssues(owner, repository, tokens))
        print("ISSUES RETRIEVED")

        print("RETRIEVING PULL_REQUESTS...")
        pullrequests = list(getPRs(owner, repository, tokens))
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
