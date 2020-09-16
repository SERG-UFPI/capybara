import datetime
import time

from api import models, serializers
from api.lib import utils
from api.lib.classifier import commit_classifier


def parseCommits(owner, repository, commits):
    repo = models.Repository.objects.get(owner=owner, repository=repository)
    for item in commits:
        try:
            commit_attributes = {}

            classification = commit_classifier.run(item["message"])
            for key in classification:
                commit_attributes[utils.toCamelCase(key)] = classification[key]

            user = item["Author"]
            i = user.find("<")
            name = user[0:i].strip()
            email = user[(i + 1) : (len(user) - 1)]

            user = {"name": name, "email": email, "repository": repo.pk}

            commit_attributes["repository"] = repo.pk

            for key in item:
                if key == "Commit":
                    commit_attributes["commiter"] = item[key]
                    continue
                if key.lower().find("date") != -1:
                    commit_attributes[utils.toCamelCase(key)] = (
                        None
                        if item[key] is None
                        else time.mktime(
                            datetime.datetime.strptime(
                                item[key], "%a %b %d %H:%M:%S %Y %z"
                            ).timetuple()
                        )
                    )
                    print(commit_attributes[utils.toCamelCase(key)])
                    continue
                commit_attributes[utils.toCamelCase(key)] = item[key]

            identification_serializer = serializers.FullIdentificationSerializer(
                data=user
            )
            if identification_serializer.is_valid():
                identification_serializer.save()

            commit_serializer = serializers.FullCommitSerializer(data=commit_attributes)
            if commit_serializer.is_valid():
                commit_serializer.save()
            else:
                print(commit_serializer.errors)
        except Exception as e:
            # print(e)
            pass
