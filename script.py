import psycopg2
from perceval.backends.core.git import Git


def getCommits(user_owner, repo_name):
    repo = Git(f"https://github.com/{user_owner}/{repo_name}.git",
               f"https://github.com/{user_owner}/{repo_name}.git")
    commits = repo.fetch()
    return commits


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

    conn.close()