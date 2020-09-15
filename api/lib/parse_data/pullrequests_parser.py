from api import serializers
from api.lib import utils
from api import models


def parsePullRequests(owner, repository, pullrequests):
    repo = models.Repository.objects.get(
        owner=owner, repository=repository)
    for item in pullrequests:
        pullrequest_attributes = {}

        pullrequest_attributes["repository"] = repo.pk

        for key in item:
            pullrequest_attributes[utils.toCamelCase(
                key)] = item[key]

        pullrequest_serializer = serializers.FullPullRequestSerializer(
            data=pullrequest_attributes)
        if pullrequest_serializer.is_valid():
            print('pr is valid')
            pullrequest_serializer.save()
