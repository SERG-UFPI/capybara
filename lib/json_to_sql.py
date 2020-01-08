from lib.create_script import createTableScript, createRelationshipCommitsRepositorysScript, createRelationshipIssuesRepositorysScript, createRelationshipPullRequestsRepositorysScript
from lib.alter_script import alterTableScript


def insertCommitsCommand(keys, values, json_file):
    sql = "INSERT INTO commits ("
    for i in range(len(keys)):
        atribute_name = keys[i].lower().replace("-", "_")
        if keys[i] == "Commit":
            atribute_name = "commiter"
        elif atribute_name == "user":
            atribute_name = "user_info"
        if i == len(keys) - 1:
            sql += f"{atribute_name}"
        else:
            sql += f"{atribute_name}, "
    sql += ") VALUES (\n"
    for i in range(len(keys)):
        # t = type(json_file[keys[i]])
        if i == len(keys) - 1:
            sql += "%s);"
        else:
            sql += "%s, "

    return sql


def _createTable(tables, keys, attributes, category, connection, cursor):
    table = 'repositorys' if category == 'repository' else category
    if table in tables:
        new_json = {}
        columns = [atrib["name"] for atrib in tables[table]]
        for key in attributes:
            name_column = key.lower()
            if name_column == "user":
                name_column = "user_info"
            if not (name_column in columns):
                new_json[key] = attributes[key]
        if len(new_json) > 0:
            keys = [key for key in new_json]
            alterTableScript(keys, cursor, new_json, table)
            connection.commit()
    else:
        createTableScript(keys, cursor, attributes, table)
        connection.commit()


def _createRelationshipTable(connection, cursor, keys):
    createRelationshipCommitsRepositorysScript(cursor, keys)
    createRelationshipIssuesRepositorysScript(cursor, keys)
    createRelationshipPullRequestsRepositorysScript(cursor, keys)
    connection.commit()


def jsonToSql(connection, tables, repository):
    print("PARSING TO SQL...")
    cursor = connection.cursor()

    owner_name = repository["repository"][0]["data"]["owner"]
    repository_name = repository["repository"][0]["data"]["repository"]

    # Criação da tabela
    for category in repository:
        attributes = {}
        for item in repository[category]:
            for key, value in item['data'].items():
                if not (value is None):
                    attributes[key] = value

        keys = [key for key in attributes]

        try:
            _createTable(tables, keys, attributes, category, connection,
                         cursor)
            print(f"CREATED TABLE {category}")
        except Exception as e:
            print(f" # Erro na criação da tabela: {e}")

    for item in repository["repository"]:
        attributes = {}
        for key, value in item['data'].items():
            if not (value is None):
                attributes[key] = value

        keys = [key for key in attributes]

        try:
            _createRelationshipTable(connection, cursor, keys)
            print(f"CREATED RELATIONSHIP TABLES")
        except Exception as e:
            print(f" # Erro na criação de tabelas de relacionamento: {e}")