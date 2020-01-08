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

    conn.close()