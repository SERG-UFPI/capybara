from django.contrib.postgres.fields import ArrayField
from django.db import models


class Repository(models.Model):
    class Meta(object):
        unique_together = (("owner", "repository"),)

    owner = models.TextField(max_length=100, blank=False, null=False)
    repository = models.TextField(max_length=100, blank=False, null=False)
    name = models.TextField(blank=True, null=True)
    mainLanguage = models.TextField(blank=True, null=True)
    language = models.TextField(blank=True, null=True)
    homepage = models.TextField(blank=True, null=True)
    ownerAvatarUrl = models.TextField(blank=True, null=True)
    forksCount = models.IntegerField(blank=True, null=True)
    fork = models.BooleanField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    defaultBranch = models.TextField(blank=True, null=True)
    createdAt = models.IntegerField(blank=True, null=True)
    cloneUrl = models.TextField(blank=True, null=True)
    fullname = models.TextField(blank=True, null=True)
    hasWiki = models.BooleanField(blank=True, null=True)
    key = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(blank=True, null=True)
    numFiles = models.IntegerField(blank=True, null=True)
    archived = models.BooleanField(blank=True, null=True)
    subscribersCount = models.IntegerField(blank=True, null=True)
    watchersCount = models.IntegerField(blank=True, null=True)
    updatedAt = models.IntegerField(blank=True, null=True)
    stargazersCount = models.IntegerField(blank=True, null=True)
    pushedAt = models.IntegerField(blank=True, null=True)
    openIssues = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Commit(models.Model):
    commit = models.TextField(primary_key=True)
    adaptivePred = models.BooleanField(blank=True, null=True)
    perfectivePred = models.BooleanField(blank=True, null=True)
    isRefactorPred = models.BooleanField(blank=True, null=True)
    parents = ArrayField(models.TextField(blank=True, null=True), blank=True, null=True)
    author = models.TextField(blank=True, null=True)
    authorDate = models.FloatField(blank=True, null=True)
    commiter = models.TextField(blank=True, null=True)
    commitDate = models.FloatField(blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    files = ArrayField(models.JSONField(blank=True, null=True), blank=True, null=True)
    merge = models.TextField(blank=True, null=True)
    correctivePred = models.BooleanField(blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class Issue(models.Model):
    id = models.TextField(primary_key=True)
    updatedAt = models.IntegerField(blank=True, null=True)
    activeLockReason = models.TextField(blank=True, null=True)
    milestone = models.JSONField(blank=True, null=True)
    author = models.JSONField(blank=True, null=True)
    labels = ArrayField(models.JSONField(blank=True, null=True), blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    assignee = ArrayField(
        models.JSONField(blank=True, null=True), blank=True, null=True
    )
    locked = models.BooleanField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    createdAt = models.IntegerField(blank=True, null=True)
    authorAssociation = models.TextField(blank=True, null=True)
    key = models.IntegerField(blank=True, null=True)
    closedAt = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    assignees = ArrayField(
        models.JSONField(blank=True, null=True), blank=True, null=True
    )
    reactions = ArrayField(
        models.JSONField(blank=True, null=True), blank=True, null=True
    )
    body = models.TextField(blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class PullRequest(models.Model):
    id = models.TextField(primary_key=True)
    url = models.TextField(blank=True, null=True)
    additions = models.IntegerField(blank=True, null=True)
    assignee = ArrayField(
        models.JSONField(blank=True, null=True), blank=True, null=True
    )
    assignees = ArrayField(
        models.JSONField(blank=True, null=True), blank=True, null=True
    )
    authorAssociation = models.TextField(blank=True, null=True)
    baseRefOid = models.TextField(blank=True, null=True)
    baseRefName = models.TextField(blank=True, null=True)
    baseRepository = models.JSONField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    changedFiles = models.IntegerField(blank=True, null=True)
    closedAt = models.IntegerField(blank=True, null=True)
    comments = models.IntegerField(blank=True, null=True)
    commits = models.IntegerField(blank=True, null=True)
    createdAt = models.IntegerField(blank=True, null=True)
    deletions = models.IntegerField(blank=True, null=True)
    isDraft = models.BooleanField(blank=True, null=True)
    headRefOid = models.TextField(blank=True, null=True)
    headRefName = models.TextField(blank=True, null=True)
    labels = ArrayField(models.JSONField(blank=True, null=True), blank=True, null=True)
    locked = models.BooleanField(blank=True, null=True)
    maintainerCanModify = models.BooleanField(blank=True, null=True)
    mergeable = models.TextField(blank=True, null=True)
    merged = models.BooleanField(blank=True, null=True)
    mergedAt = models.IntegerField(blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    state = models.TextField(blank=True, null=True)
    title = models.TextField(blank=True, null=True)
    updatedAt = models.IntegerField(blank=True, null=True)
    author = models.JSONField(blank=True, null=True)
    mergeCommit = models.JSONField(blank=True, null=True)
    mergedBy = models.JSONField(blank=True, null=True)
    milestone = models.JSONField(blank=True, null=True)
    activeLockReason = models.TextField(blank=True, null=True)
    key = models.IntegerField(blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class Identification(models.Model):
    name = models.TextField()
    email = models.TextField()
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class MapIdentification(models.Model):
    group = models.IntegerField()
    identification = models.ForeignKey(Identification, on_delete=models.CASCADE)
    algorithm = models.TextField()
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)


class Metrics(models.Model):
    ci = models.IntegerField(blank=True, null=True)
    license = models.IntegerField(blank=True, null=True)
    history = models.FloatField(blank=True, null=True)
    management = models.FloatField(blank=True, null=True)
    documentation = models.FloatField(blank=True, null=True)
    community = models.IntegerField(blank=True, null=True)
    tests = models.FloatField(blank=True, null=True)
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
