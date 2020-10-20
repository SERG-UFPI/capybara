from django.urls import path

from api import views

urlpatterns = [
    path(
        "insert/commits",
        views.InsertCommits.as_view(),
    ),
    path(
        "insert/repository",
        views.InsertRepository.as_view(),
    ),
    path(
        "insert/issues",
        views.InsertIssues.as_view(),
    ),
    path(
        "insert/pullrequests",
        views.InsertPullRequests.as_view(),
    ),
    path(
        "repositories/",
        views.GetAllRepositorys.as_view(),
    ),
    path(
        "repository/<str:owner>/<str:repository>", views.GetSingleRepository.as_view()
    ),
    path(
        "commits/<str:owner>/<str:repository>",
        views.GetRepositoryCommits.as_view(),
    ),
    path(
        "issues/<str:owner>/<str:repository>",
        views.GetRepositoryIssues.as_view(),
    ),
    path(
        "pullrequests/<str:owner>/<str:repository>",
        views.GetRepositoryPullRequests.as_view(),
    ),
    path(
        "metrics/",
        views.GetRepositoryMetrics.as_view(),
    ),
    path(
        "classify/<str:owner>/<str:repository>",
        views.GetRepositoryClassification.as_view(),
    ),
    path(
        "link_ids/local/simple/",
        views.LocalLinkRepositoryUsersSimple.as_view(),
    ),
    path(
        "link_ids/local/bird/",
        views.LocalLinkRepositoryUsersBird.as_view(),
    ),
    path(
        "link_ids/local/improved/",
        views.LocalLinkRepositoryUsersImproved.as_view(),
    ),
    path(
        "download_repository/<str:owner>/<str:repository>",
        views.DownloadSingleRepository.as_view(),
    ),
    path(
        "get_repository_users/<str:owner>/<str:repository>",
        views.GetRepositoryUsers.as_view(),
    ),
    path(
        "get_all_users",
        views.GetGlobalUsers.as_view(),
    ),
    # path(
    #     "delete_all_repositories",
    #     views.DeleteAllRepositories.as_view(),
    # ),
    path(
        "clone_repository",
        views.CloneRepository.as_view(),
    ),
    path(
        "",
        views.Home.as_view(),
        name="home",
    ),
]
