import unidecode


def run(string):
    normalized_user = unidecode.unidecode(string)
    normalized_user = normalized_user.lower()
    normalized_user = normalized_user.strip()
    normalized_user = normalized_user.replace(" ", "")
    index = normalized_user.find("@")
    if index != -1:
        normalized_user = normalized_user[0:index]
    return normalized_user
