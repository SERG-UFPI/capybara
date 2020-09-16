from api import models, serializers
from api.lib import utils


def parseIssues(owner, repository, issues):
    repo = models.Repository.objects.get(owner=owner, repository=repository)
    for item in issues:
        issue_attributes = {}

        issue_attributes["repository"] = repo.pk

        for key in item:
            issue_attributes[utils.toCamelCase(key)] = item[key]

        issue_serializer = serializers.FullIssueSerializer(data=issue_attributes)
        if issue_serializer.is_valid():
            issue_serializer.save()
