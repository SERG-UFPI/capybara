from github import RateLimitExceededException
from api.lib import utils
from . import querys


def get_repository_info(owner, repository):
    tokens = utils.get_tokens()
    repository_data = None
    query = querys.query_get_repository(owner, repository)
    result = utils.run_query(query, tokens)

    if result:
        if not result.get("data", None):
            raise RateLimitExceededException

        repository_data = result["data"]["repository"]

        repository_data = utils.parse_json([repository_data])[0]

        num_files = utils.get_num_files(owner, repository)
        print(repository_data)
        return {
            "owner_avatar_url": repository_data["owner"]["avatarUrl"],
            "owner": owner,
            "repository": repository,
            "has_wiki": repository_data["hasWikiEnabled"],
            "fullname": repository_data["nameWithOwner"],
            "clone_url": repository_data["url"],
            "created_at": repository_data["createdAt"],
            "default_branch": repository_data["defaultBranchRef"]["name"],
            "description": repository_data["description"],
            "fork": repository_data["isFork"],
            "forks_count": repository_data["forkCount"],
            "homepage": repository_data["homepageUrl"],
            "language": repository_data["primaryLanguage"]["name"],
            "main_language": repository_data["primaryLanguage"]["name"],
            "name": repository_data["name"],
            "open_issues": repository_data["issues"],
            "pushed_at": repository_data["pushedAt"],
            "stargazers_count": repository_data["stargazerCount"],
            "updated_at": repository_data["updatedAt"],
            "watchers_count": repository_data["watchers"],
            "subscribers_count": None,
            "archived": repository_data["isArchived"],
            "num_files": num_files,
            "size": repository_data["diskUsage"],
        }
