from .bird_algorithm import start_bird_algorithm
from .simple_algorithm import start_simple_algorithm
from api import serializers
from api import models
from api.lib import utils


def run(owner, repository, algorithm):
    if algorithm.lower() != "simple" and algorithm.lower() != "bird":
        raise Exception({"error": "Algorithm does not exist"})

    try:
        repository_retrieved = models.Repository.objects.get(
            owner=owner, repository=repository)
        map_identification_retrieved = models.MapIdentification.objects.filter(
            repository=repository_retrieved.pk)
        map_identification_list = []
        if map_identification_retrieved.exists():
            map_identification_list = [utils.without_keys(
                item, ['id', 'repository_id']) for item in map_identification_retrieved.values()]

            for item in map_identification_list:
                _user = models.Identification.objects.filter(
                    repository=repository_retrieved.pk).get(id=item['identification_id'])

                item['name'] = _user.name
                item['email'] = _user.email

                del item['identification_id']

            return map_identification_list
        else:
            users_identification_retrieved = models.Identification.objects.filter(
                repository=repository_retrieved.pk)
            if users_identification_retrieved.exists():
                users_list = list(users_identification_retrieved.values())
                result = None
                if algorithm.lower() == "simple":
                    result = start_simple_algorithm(users_list)
                else:
                    result = start_bird_algorithm(users_list)

                map_identification = []
                for key in result:
                    for user in result[key]:
                        _item = {
                            'group': key,
                            'identification': user['id'],
                            'name': user['name'],
                            'email': user['email'],
                            'algorithm': algorithm,
                            'repository': repository_retrieved.pk
                        }

                        serializer = serializers.MapIdentificationSerializer(
                            data=_item)
                        if serializer.is_valid():
                            serializer.save()

                        map_identification.append(utils.without_keys(
                            _item, ['identification', 'repository']))

                return map_identification

            else:
                raise Exception(
                    {'error': 'No users founded for target repository'})
    except models.Repository.DoesNotExist as e:
        raise e

    # insert in db

    # print(f"Resultado busca 1: {tables}")
    # print(type(tables))

    map_identification = []

    # if tables != None and len(tables) > 0:
    #     # print("Entrou")
    #     for t in tables:
    #         item = {
    #             "id": t[0],
    #             "name": t[1],
    #             "email": t[2],
    #             "algorithm": t[3]
    #         }
    #         map_identification.append(item)

    #     # print(map_identification)
    #     conn.close()
    #     return {"map_identification": map_identification}

    # sql = f"""SELECT
    #         id, name, email
    #     FROM
    #         identification
    #     WHERE
    #         identification.owner = \'{user_owner}\' AND
    #         identification.repository = \'{repo_name}\'
    #     ;"""

    # cursor.execute(sql)
    # tables = cursor.fetchall()

    # users = []
    # for user in tables:
    #     users.append(
    #         {
    #             "id": user[0],
    #             "name": user[1],
    #             "email": user[2]
    #         }
    #     )
    # # print(users)

    # result = None

    # if algo.lower() == "simple":
    #     result = start_simple_algorithm(users=users)
    #     # print(result)
    #     _insertMapIdentification(result, "SIMPLE", user_owner, repo_name, conn)
    # else:
    #     result = start_bird_algorithm(users=users)
    #     # print(result)
    #     _insertMapIdentification(result, "BIRD", user_owner, repo_name, conn)

    # # print(f"Resultado: {result}")

    # # print(sql_result)

    # cursor.execute(sql_result)
    # tables = cursor.fetchall()

    # # print(f"Resultado busca 2: {tables}")

    # map_identification = []

    # if tables != None and len(tables) > 0:
    #     for t in tables:
    #         item = {
    #             "id": t[0],
    #             "name": t[1],
    #             "email": t[2],
    #             "algorithm": t[3]
    #         }
    #         map_identification.append(item)

    #     # print(map_identification)
    #     conn.close()
    #     return {"map_identification": map_identification}
    # conn.close()
