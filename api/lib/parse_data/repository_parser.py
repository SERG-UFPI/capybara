from api import serializers
from api.lib import utils


def parse_repositorys(repository_info):
    repository_attributes = {}

    for key in repository_info:
        repository_attributes[utils.to_camel_case(key)] = repository_info[key]

    repository_serializer = serializers.FullRepositorySerializer(
        data=repository_attributes
    )

    if repository_serializer.is_valid():
        repository_serializer.save()
