import json
import os
import psycopg2
from lib.create_script import createTableScript, createRelationshipCommitsRepositorysScript, createRelationshipIssuesRepositorysScript, createRelationshipPullRequestsRepositorysScript
from lib.alter_script import alterTableScript
from id_linking_algorithms.simple_algorithm import start_simple_algorithm
from id_linking_algorithms.bird_algorithm import start_bird_algorithm
from id_linking_algorithms.normalizer import normalizer


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
            sql += "%s) ON CONFLICT DO NOTHING;"
        else:
            sql += "%s, "

    return sql


def insertIssuesCommand(keys, values, json_file):
    sql = "INSERT INTO issues ("
    for i in range(len(keys)):
        atribute_name = keys[i].lower().replace("-", "_")
        if atribute_name == "user":
            atribute_name = "user_info"
        if i == len(keys) - 1:
            sql += f"{atribute_name}"
        else:
            sql += f"{atribute_name}, "
    sql += ") VALUES (\n"
    for i in range(len(keys)):
        if i == len(keys) - 1:
            sql += "%s) ON CONFLICT DO NOTHING;"
        else:
            sql += "%s, "

    return sql


def insertPRsCommand(keys, values, json_file):
    sql = "INSERT INTO pullrequests ("
    for i in range(len(keys)):
        atribute_name = keys[i].lower().replace("-", "_")
        if atribute_name == "user":
            atribute_name = "user_info"
        if i == len(keys) - 1:
            sql += f"{atribute_name}"
        else:
            sql += f"{atribute_name}, "
    sql += ") VALUES (\n"
    for i in range(len(keys)):
        if i == len(keys) - 1:
            sql += "%s) ON CONFLICT DO NOTHING;"
        else:
            sql += "%s, "

    return sql


def insertRepositorysCommand(keys, values, json_file):
    sql = "INSERT INTO repositorys ("
    for i in range(len(keys)):
        atribute_name = keys[i].lower().replace("-", "_")
        if atribute_name == "user":
            atribute_name = "user_info"
        if i == len(keys) - 1:
            sql += f"{atribute_name}"
        else:
            sql += f"{atribute_name}, "
    sql += ") VALUES (\n"
    for i in range(len(keys)):
        if i == len(keys) - 1:
            sql += "%s) ON CONFLICT DO NOTHING;"
        else:
            sql += "%s, "

    return sql


# def insertRepositorysRelationshipCommand():
#     sql = f"""
#         INSERT INTO
#             repository_commits_issues_pullrequests (owner, repository, commit, id_issue, id_pull_request,)
#         VALUES
#             (%s, %s);
#     """
#     return sql


def insertRepositorysRelationshipCommand(cursor, values, table_referenced):
    relationship_table = ""
    atributte = ""
    if table_referenced == "issues":
        relationship_table = "repository_issues"
        atributte = "id_issue"
    elif table_referenced == "pullrequests":
        relationship_table = "repository_pullrequests"
        atributte = "id_pull_request"
    elif table_referenced == "commits":
        relationship_table = "repository_commits"
        atributte = "commit"
    sql = f"""
    INSERT INTO {relationship_table} (owner, repository, {atributte})
    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;"""

    cursor.execute(sql, values)


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


def _insert(new_values, keys, values, attributes, cursor, connection,
            category):
    table = 'repositorys' if category == 'repository' else category
    if table == "commits":
        sql = insertCommitsCommand(keys, values, attributes)
    elif table == "issues":
        sql = insertIssuesCommand(keys, values, attributes)
    elif table == "pullrequests":
        sql = insertPRsCommand(keys, values, attributes)
    elif table == "repositorys":
        sql = insertRepositorysCommand(keys, values, attributes)

    cursor.execute(sql, new_values)
    connection.commit()


def _createIdentificationTables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identification (
            id BIGSERIAL UNIQUE,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            PRIMARY KEY (name, email)
        );
    """)
    connection.commit()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_identification (
            id BIGSERIAL,
            id_identification INTEGER REFERENCES identification(id),
            algorithm VARCHAR NOT NULL,
            PRIMARY KEY (id, id_identification)
        );
    """)
    connection.commit()


def _insertUser(user, connection):
    cursor = connection.cursor()
    id_row = None
    sql = """
    INSERT INTO
        identification (name, email)
    VALUES
        (%s, %s)
    ON CONFLICT DO NOTHING
    RETURNING id;
    """
    cursor.execute(sql, (user["name"], user["email"]))
    returned_value = cursor.fetchone()
    if returned_value:
        id_row = returned_value[0]
    connection.commit()
    return id_row


def _getExistUsers(connection):
    sql = """
        SELECT
            *
        FROM
            identification
        ;
    """
    result = []
    cursor = connection.cursor()
    cursor.execute(sql)
    elements = cursor.fetchall()
    for element in elements:
        if len(element) > 0:
            result.append(element)
    return result


def _getExistMaps(connection, algorithm):
    sql = f"""
        SELECT
            json_build_object(map_identification.id, json_agg((identification.id, identification.name, identification.email)))
        FROM
            map_identification, identification
        WHERE
            map_identification.id_identification = identification.id AND map_identification.algorithm = '{algorithm}'
        GROUP BY
            map_identification.id
        ;
    """
    result = []
    cursor = connection.cursor()
    cursor.execute(sql)
    elements = cursor.fetchall()
    for element in elements:
        e = element[0]
        key = int(list(e.keys())[0])
        temp = {key: []}
        for i in e.values():
            for j in i:
                temp[key].append(
                    {"id": j["f1"], "name": j["f2"], "email": j["f3"], "normalized": normalizer(j["f3"])})
        if len(temp) > 0:
            result.append(temp)

    return result


def _insertMapIdentification(map_identification, algorithm, connection):
    cursor = connection.cursor()
    # print(map_identification)
    for i in map_identification:
        # print(i)
        for value in list(i.values())[0]:
            id_value = int(list(i.keys())[0])
            sql = """
                INSERT INTO
                    map_identification (id, id_identification, algorithm)
                VALUES
                    (%s, %s, %s)
                ON CONFLICT DO NOTHING;
            """
            cursor.execute(sql, (id_value, value["id"], algorithm))
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
            print(f" # Erro na criação da tabela {category}: {e}")

    _createIdentificationTables(connection)

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

    # Inserção de items do db
    for category in repository:
        users = []
        attributes = {}
        for item in repository[category]:
            attributes = item['data']
            if category == "commits":
                # print(attributes)
                user = attributes["Commit"]
                i = user.find("<")
                name = user[0:i].strip()
                email = user[(i + 1):(len(user) - 1)]
                user = {"name": name, "email": email}
                id_user = _insertUser(user, connection)
                # print(f"ID_USER ==> {id_user}")
                if id_user:
                    user["id"] = id_user
                    # print(user)
                    users.append(user)
            keys = []
            for key in attributes:
                if attributes[key] is not None:
                    keys.append(key)

            values = []
            for key in attributes:
                if attributes[key] is not None:
                    values.append(attributes[key])

            new_values = [
                json.dumps(v, ensure_ascii=False) if
                (type(v) is dict or type(v) is list) else v for v in values
            ]

            try:
                _insert(new_values, keys, values, attributes, cursor,
                        connection, category)
                if category != "repository":
                    if category == "commits":
                        insertRepositorysRelationshipCommand(
                            cursor, (owner_name, repository_name,
                                     attributes["commit"]), category)
                    else:
                        insertRepositorysRelationshipCommand(
                            cursor,
                            (owner_name, repository_name, attributes["id"]),
                            category)

                print(f"INSERTED DATA IN DB {category}")
            except Exception as e:
                print(f" # Erro na inserção de dados: {e}")
        if category == "commits":
            maps_existent = _getExistMaps(connection, "Simple")
            map_identification_simple = start_simple_algorithm(
                users, maps_existent=maps_existent)
            _insertMapIdentification(
                map_identification_simple, "Simple", connection)

            maps_existent = _getExistMaps(connection, "Bird")
            map_identification_simple = start_bird_algorithm(
                users, maps_existent=maps_existent)
            _insertMapIdentification(
                map_identification_simple, "Bird", connection)
