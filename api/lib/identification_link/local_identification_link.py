from api import models, serializers
from api.lib import utils

from api.lib.identification_link.bird_algorithm import start_bird_algorithm
from api.lib.identification_link.simple_algorithm import start_simple_algorithm
from api.lib.identification_link.improved_algorithm import start_improved_algorithm


def run(owner, repository, algorithm):
    if (
        algorithm.lower() != "simple"
        and algorithm.lower() != "bird"
        and algorithm.lower() != "improved"
    ):
        raise Exception({"error": "Algorithm does not exist"})

    repository_retrieved = models.Repository.objects.get(
        owner=owner, repository=repository
    )
    map_identification_retrieved = models.LocalMapIdentification.objects.filter(
        repository=repository_retrieved.pk, algorithm=algorithm
    )
    map_identification_list = []
    if map_identification_retrieved.exists():
        map_identification_list = [
            utils.without_keys(item, ["id", "repository_id"])
            for item in map_identification_retrieved.values()
        ]

        for item in map_identification_list:
            _user = models.Identification.objects.filter(
                repository=repository_retrieved.pk
            ).get(id=item["identification_id"])
            item["name"] = _user.name
            item["email"] = _user.email

            del item["identification_id"]

        return map_identification_list

    users_identification_retrieved = models.Identification.objects.filter(
        repository=repository_retrieved.pk
    )
    if users_identification_retrieved.exists():
        users_list = list(users_identification_retrieved.values())
        result = None
        if algorithm.lower() == "simple":
            result = start_simple_algorithm(users_list)
        elif algorithm.lower() == "bird":
            result = start_bird_algorithm(users_list)
        elif algorithm.lower() == "improved":
            result = start_improved_algorithm(users_list)

        map_identification = []
        for key in result:
            for user in result[key]:
                _item = {
                    "group": key,
                    "identification": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "algorithm": algorithm,
                    "repository": repository_retrieved.pk,
                }

                serializer = serializers.LocalMapIdentificationSerializer(data=_item)
                if serializer.is_valid():
                    serializer.save()

                map_identification.append(
                    utils.without_keys(_item, ["identification", "repository"])
                )

        return map_identification

    raise models.Identification.DoesNotExist("No users founded for target repository")
