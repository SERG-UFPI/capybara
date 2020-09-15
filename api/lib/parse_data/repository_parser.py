from api import serializers
from api.lib import utils
from api import models


def parseRepositorys(repository_info):
    repository_attributes = {}

    for key in repository_info:
        repository_attributes[utils.toCamelCase(
            key)] = repository_info[key]

    repository_serializer = serializers.FullRepositorySerializer(
        data=repository_attributes)

    if repository_serializer.is_valid():
        repository_serializer.save()
