import psycopg2

if __name__ == "__main__":
    connection = psycopg2.connect(
        "dbname=teste user=postgres password=maxlima13")

    cursor = connection.cursor()
    sql_user = """
        INSERT INTO identification (name, email) VALUES (%s, %s);
    """

    sql_map = """
      INSERT INTO map_identification (id_identification, algorithm) VALUES (%s, %s);
    """

    users = [
        ("Max", "max.lima2@gmail.com"),
        ("Max", "max.lima3@gmail.com"),
        ("Max", "max.lima.1@gmail.com"),
        ("Joao", "max.lima2@gmail.com"),
        ("Nicolas", "max.lima2@gmail.com"),
        ("Roberto", "max.lima2@gmail.com"),
    ]

    _map = [
        (),
    ]

    for user in users:
        cursor.execute(sql_user, (user[0], user[1]))
        connection.commit()
    for map_v in _maps:
        cursor.execute(sql_map, (map_v[0], map_v[1]))
        connection.commit()
