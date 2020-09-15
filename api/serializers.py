from rest_framework import serializers
from api import models


class FullCommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Commit
        fields = '__all__'

    def create(self, validated_data):
        commit, created = models.Commit.objects.update_or_create(
            **validated_data)
        return commit


class FullIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = '__all__'

    def create(self, validated_data):
        issue, created = models.Issue.objects.update_or_create(
            **validated_data)
        return issue


class FullPullRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PullRequest
        fields = '__all__'

    def create(self, validated_data):
        pullrequest, created = models.PullRequest.objects.update_or_create(
            **validated_data)
        return pullrequest


class FullRepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repository
        fields = '__all__'

    def create(self, validated_data):
        repository, created = models.Repository.objects.update_or_create(
            **validated_data)
        return repository

    def update(self, repository, validated_data):
        repository.metrics = validated_data.get('metrics', repository.metrics)
        return repository


class FullIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Identification
        fields = '__all__'

    def create(self, validated_data):
        identification, created = models.Identification.objects.update_or_create(
            **validated_data)
        return identification


class RepositoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repository
        fields = ['owner', 'repository',
                  'ownerAvatarUrl', 'description', 'language']


class RepositorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Repository
        fields = ['owner', 'repository']


class MetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Metrics
        fields = '__all__'

    def create(self, validated_data):
        metrics, created = models.Metrics.objects.update_or_create(
            **validated_data)

        return metrics


class MapIdentificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MapIdentification
        fields = '__all__'

    def create(self, validated_data):
        map_identification, created = models.MapIdentification.objects.update_or_create(
            **validated_data)

        return map_identification