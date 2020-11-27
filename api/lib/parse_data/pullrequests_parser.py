from api import models, serializers
from api.lib import utils
from api.lib.feeback_to_admin import send_feedback


def parse_pullrequests(owner, repository, pullrequests):
    repo = models.Repository.objects.get(owner=owner, repository=repository)
    for index in range(len(pullrequests)):
        pullrequest_attributes = {}

        pullrequest_attributes["repository"] = repo.pk

        for key in pullrequests[index]:
            _value = pullrequests[index].get(key, None)
            pullrequest_attributes[utils.to_camel_case(key)] = _value

        try:
            pullrequest_serializer = serializers.FullPullRequestSerializer(
                data=pullrequest_attributes
            )
            if pullrequest_serializer.is_valid():
                pullrequest_serializer.save()
        except Exception as error:
            send_feedback.send(f"Error {error}")
