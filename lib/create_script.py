def createTableScript(keys, cursor, json_file, table):
    sql = """"""
    sql += f"CREATE TABLE IF NOT EXISTS {table} (\n"
    sql += " key BIGSERIAL"
    for key in keys:
        t = type(json_file[key])
        atribute_name = key.lower().replace("-", "_")
        if key == "Commit":
            atribute_name = "commiter"
        if atribute_name == "user":
            atribute_name = "user_info"
        if t is bool:
            sql += f",\n {atribute_name} BOOLEAN"
        elif t is str:
            sql += f",\n {atribute_name} TEXT"
        elif t is list or t is dict:
            sql += f",\n {atribute_name} JSON"
        elif t is int:
            sql += f",\n {atribute_name} INTEGER"
        elif t is float:
            sql += f",\n {atribute_name} DECIMAL"
    if table != "repositorys":
        if table == "commits":
            sql += ",\n  PRIMARY KEY (commit)"
        else:
            sql += ",\n  PRIMARY KEY (id)"
    else:
        sql += ",\n  PRIMARY KEY (owner, repository)"
        # sql += f",\n PRIMARY KEY ("
        # for key in keys:
        #     if key == keys[-1]:
        #         sql += f"{key})"
        #     else:
        #         sql += f"{key}, "
    sql += "\n);"
    # print(sql)
    cursor.execute(sql)


def createRelationshipCommitsRepositorysScript(cursor, repository_keys):
    sql = """
    CREATE TABLE IF NOT EXISTS repository_commits (
        key BIGSERIAL,
        commit TEXT"""

    # for key in repository_keys:
    #     sql += f",\n\t{key} TEXT"
    sql += ",\n\towner TEXT"
    sql += ",\n\trepository TEXT,"

    sql += """
        FOREIGN KEY (commit) REFERENCES commits (commit)"""

    sql += f",\n\tFOREIGN KEY (owner, repository) REFERENCES repositorys (owner, repository)"

    sql += """,
        PRIMARY KEY (commit, owner, repository"""

    # for key in repository_keys:
    #     sql += f", {key}"

    sql += ")\n);"

    cursor.execute(sql)


def createRelationshipIssuesRepositorysScript(cursor, repository_keys):
    sql = """
    CREATE TABLE IF NOT EXISTS repository_issues (
        key BIGSERIAL,
        id_issue VARCHAR(100)"""

    # for key in repository_keys:
    #     sql += f",\n\t{key} TEXT"
    sql += ",\n\towner TEXT"
    sql += ",\n\trepository TEXT,"

    sql += """
        FOREIGN KEY (id_issue) REFERENCES issues (id)"""

    sql += f",\n\tFOREIGN KEY (owner, repository) REFERENCES repositorys (owner, repository)"

    sql += """,
        PRIMARY KEY (id_issue, owner, repository"""

    # for key in repository_keys:
    #     sql += f", {key}"

    sql += ")\n);"

    cursor.execute(sql)


def createRelationshipPullRequestsRepositorysScript(cursor, repository_keys):
    sql = """
    CREATE TABLE IF NOT EXISTS repository_pullrequests (
        key BIGSERIAL,
        id_pull_request VARCHAR(100)"""

    # for key in repository_keys:
    #     sql += f",\n\t{key} TEXT"
    sql += ",\n\towner TEXT"
    sql += ",\n\trepository TEXT,"

    sql += """
        FOREIGN KEY (id_pull_request) REFERENCES pullrequests (id)"""

    sql += f",\n\tFOREIGN KEY (owner, repository) REFERENCES repositorys (owner, repository)"

    sql += """,
        PRIMARY KEY (id_pull_request, owner, repository"""

    # for key in repository_keys:
    #     sql += f", {key}"

    sql += ")\n);"

    cursor.execute(sql)
