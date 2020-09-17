from rest_framework import status
from rest_framework.response import Response

from api import models, serializers


def run():
    repositories_retrieved = list(models.Repository.objects.all().values())
    if repositories_retrieved:
        try:
            commits_retrieved = list(models.Commit.objects.all().values())

        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(
            {"error": "No repository found"}, status=status.HTTP_404_NOT_FOUND
        )
