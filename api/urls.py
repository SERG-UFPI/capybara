from django.urls import path

from . import views

urlpatterns = [
    path("insert/", views.InsertRepository.as_view()),
    path("repositories/", views.GetAllRepositorys.as_view()),
    path(
        "repository/<str:owner>/<str:repository>", views.GetSingleRepository.as_view()
    ),
    path("commits/<str:owner>/<str:repository>", views.GetRepositoryCommits.as_view()),
    path("issues/<str:owner>/<str:repository>", views.GetRepositoryIssues.as_view()),
    path(
        "pullrequests/<str:owner>/<str:repository>",
        views.GetRepositoryPullRequests.as_view(),
    ),
    path("metrics/", views.GetRepositoryMetrics.as_view()),
    path(
        "classify/<str:owner>/<str:repository>",
        views.GetRepositoryClassification.as_view(),
    ),
    path("link_ids/simple/", views.LinkRepositoryUsersSimple.as_view()),
    path("link_ids/bird/", views.LinkRepositoryUsersBird.as_view()),
    path("", views.Home.as_view(), name="home"),
]
