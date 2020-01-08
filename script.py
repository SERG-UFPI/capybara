import psycopg2
from perceval.backends.core.git import Git
from perceval.backends.core.github import GitHub


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


def run(owner, repository):
    data_base_url = os.environ.get("DATABASE_URL")
    conn = psycopg2.connect(data_base_url, sslmode='require')

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

        repository_info = list(generateRepository(owner, repository))

        print("RETRIEVING COMMITS...")
        commits = list(getCommits(owner, repository))
        print("COMMITS RETRIEVED")

        print("RETRIEVING ISSUES...")
        issues = list(getIssues(owner, repository, tokens))
        print("ISSUES RETRIEVED")

        print("RETRIEVING PULL_REQUESTS...")
        pullrequests = list(getPRs(owner, repository, tokens))
        print("PULL_REQUESTS RETRIEVED")

    conn.close()