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

    conn.close()