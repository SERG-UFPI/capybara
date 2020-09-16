from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api import models, serializers
from api.lib import utils
from api.lib.classifier import repository_classifier
from api.lib.classifier.get_metrics import get_all_metrics
from api.lib.get_data.get_repository_data import Retriever
from api.lib.identification_link import identification_link
from api.lib.parse_data.parse_repository_data import Parser


class Home(generic.TemplateView):
    template_name = "home.html"


class GetAllRepositorys(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request):
        """
        Return a list of repositories from the server database
        """
        repositories = models.Repository.objects.all()
        serializer = serializers.RepositoriesSerializer(repositories, many=True)
        return Response({"repositories": serializer.data})


class GetSingleRepository(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request, owner, repository):
        """
        Return repository detailed information
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.FullRepositorySerializer(repository_retrieved)
        return Response(serializer.data)


class InsertRepository(CreateAPIView):
    serializer_class = serializers.RepositorySerializer

    @swagger_auto_schema(tags=["Endpoints"])
    def post(self, request):
        """
        Insert a new repository to server database
        """
        owner = request.data.get("owner", None)
        repository = request.data.get("repository", None)

        if not owner or not repository:
            return Response(
                {"error": "owner or repository field do not should be null"}
            )

        retriever = Retriever(owner=owner, repository=repository)
        try:
            retriever.start()
            repository_data = {
                "repository_info": retriever.repository_info,
                "commits": retriever.commits,
                "issues": retriever.issues,
                "pullrequests": retriever.pullrequests,
            }

            parser = Parser(
                owner=owner,
                repository=repository,
                repository_info=repository_data["repository_info"],
                commits=repository_data["commits"],
                issues=repository_data["issues"],
                pullrequests=repository_data["pullrequests"],
            )
            parser.start()

            return Response({"success": True})
        except Exception as error:
            print(f"Error on retrieve {error}")
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetRepositoryMetrics(CreateAPIView):
    serializer_class = serializers.RepositorySerializer

    @swagger_auto_schema(tags=["Endpoints"])
    def post(self, request):
        """
        Return metrics information from target repository
        """
        owner = request.data.get("owner", None)
        repository = request.data.get("repository", None)

        if not owner or not repository:
            return Response(
                {"error": "owner or repository field do not should be null"}
            )

        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            if models.Metrics.objects.filter(
                repository=repository_retrieved.pk
            ).exists():
                metrics = models.Metrics.objects.get(repository=repository_retrieved.pk)
                serializer = serializers.MetricsSerializer(metrics)

                return Response(
                    {"metrics": utils.without_keys(serializer.data, ["repository"])}
                )
            else:
                try:
                    metrics_data = get_all_metrics(owner=owner, repository=repository)
                    metrics_data["repository"] = repository_retrieved.pk

                    serializer = serializers.MetricsSerializer(data=metrics_data)
                    if serializer.is_valid():
                        serializer.save()

                    return Response(
                        {"metrics": utils.without_keys(metrics_data, ["repository"])}
                    )
                except Exception as error:
                    print(f"error: {error}")
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetRepositoryCommits(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request, owner, repository):
        """
        Return a list of commits from target repository
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            commits_retrieved = models.Commit.objects.filter(
                repository=repository_retrieved.pk
            ).values()

            return Response(
                {
                    "totalCount": len(commits_retrieved),
                    "commits": [
                        utils.without_keys(item, ["repository_id"])
                        for item in commits_retrieved
                    ],
                }
            )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetRepositoryIssues(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request, owner, repository):
        """
        Return a list of issues from target repository
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            issues_retrieved = models.Issue.objects.filter(
                repository=repository_retrieved.pk
            ).values()

            return Response(
                {
                    "totalCount": len(issues_retrieved),
                    "issues": [
                        utils.without_keys(item, ["repository_id"])
                        for item in issues_retrieved
                    ],
                }
            )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetRepositoryPullRequests(APIView):
    @swagger_auto_schema(
        tags=["Endpoints"],
    )
    def get(self, request, owner, repository):
        """
        Return a list of pullrequests from target repository
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            pullrequests_retrieved = models.PullRequest.objects.filter(
                repository=repository_retrieved.pk
            ).values()

            return Response(
                {
                    "totalCount": len(pullrequests_retrieved),
                    "pullrequests": [
                        utils.without_keys(item, ["repository_id"])
                        for item in pullrequests_retrieved
                    ],
                }
            )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetRepositoryClassification(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request, owner, repository):
        """
        Return `true` if repository is a valid repository for studies or `false` otherwise
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            if models.Metrics.objects.filter(
                repository=repository_retrieved.pk
            ).exists():
                metrics = models.Metrics.objects.get(repository=repository_retrieved.pk)
                serializer = serializers.MetricsSerializer(metrics)
                result = repository_classifier.run(
                    utils.without_keys(serializer.data, ["repository", "id"])
                )
                return Response({"is_valid": result})
            else:
                return Response(
                    {"error": "no metrics found for this repository"},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class GetRepositoryUsers(APIView):
    @swagger_auto_schema(tags=["Endpoints"])
    def get(self, request, owner, repository):
        """
        Return a list of users from target repository
        """
        try:
            repository_retrieved = models.Repository.objects.get(
                owner=owner, repository=repository
            )
            pullrequests_retrieved = models.PullRequest.objects.filter(
                repository=repository_retrieved.pk
            ).values()

            return Response(
                {
                    "totalCount": len(pullrequests_retrieved),
                    "pullrequests": pullrequests_retrieved,
                }
            )
        except models.Repository.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class LinkRepositoryUsersSimple(CreateAPIView):
    serializer_class = serializers.RepositorySerializer

    @swagger_auto_schema(tags=["Endpoints"])
    def post(self, request):
        """
        Return a list of users with links from target repository
        """
        owner = request.data.get("owner", None)
        repository = request.data.get("repository", None)

        if not owner or not repository:
            return Response(
                {"error": "owner or repository field do not should be null"}
            )

        try:
            result = identification_link.run(owner, repository, "SIMPLE")
            return Response({"map_identification": result})
        except Exception as error:
            return Response(error, status=status.HTTP_404_NOT_FOUND)


class LinkRepositoryUsersBird(CreateAPIView):
    serializer_class = serializers.RepositorySerializer

    @swagger_auto_schema(tags=["Endpoints"])
    def post(self, request):
        """
        Return a list of users with links from target repository
        """
        owner = request.data.get("owner", None)
        repository = request.data.get("repository", None)

        if not owner or not repository:
            return Response(
                {"error": "owner or repository field do not should be null"}
            )

        try:
            result = identification_link.run(owner, repository, "BIRD")
            return Response({"map_identification": result})
        except Exception as error:
            return Response(status=status.HTTP_404_NOT_FOUND)


# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404
