import json
import os
import psycopg2
from lib.create_script import createTableScript, createRelationshipCommitsRepositorysScript, createRelationshipIssuesRepositorysScript, createRelationshipPullRequestsRepositorysScript
from lib.alter_script import alterTableScript
from lib.commit_classifier import classifiy_commits_df
import sys


def print_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", err, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", err.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", err.pgerror)
    print("pgcode:", err.pgcode, "\n")


def insertCommitsCommand(keys):
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
        if i == len(keys) - 1:
            sql += "%s) ON CONFLICT DO NOTHING;"
        else:
            sql += "%s, "

    return sql


def insertIssuesCommand(keys):
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


def insertPRsCommand(keys):
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


def insertRepositorysCommand(keys):
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
    if category == "commits":
        attributes['corrective_pred'] = False
        attributes['is_refactor_pred'] = False
        attributes['perfective_pred'] = False
        attributes['adaptive_pred'] = False

        keys.append('corrective_pred')
        keys.append('is_refactor_pred')
        keys.append('perfective_pred')
        keys.append('adaptive_pred')

    if table in tables:
        print(f"Alterando tabela {table}")
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
            print(f"New keys to add to table {table}: {keys}")
            alterTableScript(keys, cursor, new_json, table)
    else:
        print("1 ==> Entrou no script de criação da tabela")
        createTableScript(keys, cursor, attributes, table)


def _createRelationshipTable(connection, cursor, keys):
    createRelationshipCommitsRepositorysScript(cursor, keys)
    createRelationshipIssuesRepositorysScript(cursor, keys)
    createRelationshipPullRequestsRepositorysScript(cursor, keys)


def _insert(new_values, keys, values, attributes, cursor, connection,
            category):
    table = 'repositorys' if category == 'repository' else category
    if table == "commits":
        sql = insertCommitsCommand(keys)
    elif table == "issues":
        sql = insertIssuesCommand(keys)
    elif table == "pullrequests":
        sql = insertPRsCommand(keys)
    elif table == "repositorys":
        sql = insertRepositorysCommand(keys)

    cursor.execute(sql, new_values)


def _createIdentificationTables(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS identification (
            owner TEXT,
            repository TEXT,
            id BIGSERIAL UNIQUE,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            PRIMARY KEY (owner, repository, name, email)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS map_identification (
            id BIGSERIAL,
            owner TEXT,
            repository TEXT,
            id_identification INTEGER REFERENCES identification(id),
            algorithm TEXT NOT NULL,
            PRIMARY KEY (id, owner, repository, id_identification)
        );
    """)


def _insertUser(user, repo, connection):
    cursor = connection.cursor()
    id_row = None
    sql = """
    INSERT INTO
        identification (name, email, owner, repository)
    VALUES
        (%s, %s, %s, %s)
    ON CONFLICT DO NOTHING
    RETURNING id;
    """
    cursor.execute(sql, (user["name"], user["email"],
                         repo["owner"], repo["repository"]))
    returned_value = cursor.fetchone()
    if returned_value:
        id_row = returned_value[0]
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


# def _getExistMaps(connection, algorithm):
#     sql = f"""
#         SELECT
#             json_build_object(map_identification.id, json_agg((identification.id, identification.name, identification.email)))
#         FROM
#             map_identification, identification
#         WHERE
#             map_identification.id_identification = identification.id AND map_identification.algorithm = '{algorithm}'
#         GROUP BY
#             map_identification.id
#         ;
#     """
#     result = []
#     cursor = connection.cursor()
#     cursor.execute(sql)
#     elements = cursor.fetchall()
#     for element in elements:
#         e = element[0]
#         key = int(list(e.keys())[0])
#         temp = {key: []}
#         for i in e.values():
#             for j in i:
#                 temp[key].append({
#                     "id": j["f1"],
#                     "name": j["f2"],
#                     "email": j["f3"],
#                     "normalized": normalizer(j["f3"])
#                 })
#         if len(temp) > 0:
#             result.append(temp)

#     return result


def jsonToSql(connection, tables, repository):
    print("PARSING TO SQL...")
    cursor = connection.cursor()

    owner_name = repository["repository"][0]["owner"]
    repository_name = repository["repository"][0]["repository"]

    # Criação da tabela
    for category in repository:
        attributes = {}
        for item in repository[category]:
            for key, value in item.items():
                if not (value is None):
                    attributes[key] = value

        keys = [key for key in attributes]
        print(keys)

        try:
            _createTable(tables, keys, attributes, category, connection,
                         cursor)
            print(f"CREATED TABLE {category}")
        except Exception as e:
            print_psycopg2_exception(e)
            print(f" # Erro na criação da tabela {category}: {e}")

    _createIdentificationTables(connection)

    for item in repository["repository"]:
        attributes = {}
        for key, value in item.items():
            if not (value is None):
                attributes[key] = value

        keys = [key for key in attributes]

        try:
            _createRelationshipTable(connection, cursor, keys)
            print(f"CREATED RELATIONSHIP TABLES")
        except Exception as e:
            print_psycopg2_exception(e)
            print(f" # Erro na criação de tabelas de relacionamento: {e}")

    # Inserção de items do db
    for category in repository:
        users = []
        attributes = {}
        for item in repository[category]:
            attributes = item

            if category == "commits":
                classification = classifiy_commits_df(attributes["message"])

                for key in classification:
                    attributes[key] = classification[key]

                user = attributes["Commit"]
                i = user.find("<")
                name = user[0:i].strip()
                email = user[(i + 1):(len(user) - 1)]
                user = {"name": name, "email": email}
                repo = {"owner": owner_name, "repository": repository_name}
                id_user = _insertUser(user, repo, connection)
                if id_user:
                    user["id"] = id_user
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
        # if category == "commits":
        #     maps_existent = _getExistMaps(connection, "Simple")
        #     map_identification_simple = start_simple_algorithm(
        #         users, maps_existent=maps_existent)
        #     _insertMapIdentification(map_identification_simple, "Simple",
        #                              connection)

        #     maps_existent = _getExistMaps(connection, "Bird")
        #     map_identification_simple = start_bird_algorithm(
        #         users, maps_existent=maps_existent)
        #     _insertMapIdentification(map_identification_simple, "Bird",
        #                              connection)
