from github import Github
from api.lib import utils


def get_repository_info(owner, repository):
    _token = utils.get_best_token()
    github = Github(_token)
    repo = github.get_repo(f"{owner}/{repository}")

    owner_avatar_url = repo.owner.avatar_url
    fullname = repo.full_name
    clone_url = repo.clone_url
    created_at = repo.created_at.timestamp()
    default_branch = repo.default_branch
    description = repo.description
    fork = repo.fork
    forks_count = repo.forks_count
    homepage = repo.homepage
    language = repo.language
    name = repo.name
    open_issues = repo.open_issues
    pushed_at = repo.pushed_at.timestamp()
    archived = repo.archived
    stargazers_count = repo.stargazers_count
    updated_at = repo.updated_at.timestamp()
    watchers_count = repo.watchers_count
    has_wiki = repo.has_wiki
    # num_authors = repo.get_collaborators().totalCount
    subscribers_count = repo.subscribers_count
    size = repo.size

    # A linguagem com o maior número de linhas de código será a main_language
    aux = repo.get_languages()
    aux = {k: v for k, v in sorted(aux.items(), key=lambda item: item[1])}
    main_language = list(aux.keys())[-1]

    num_files = utils.get_num_files(owner, repository)

    return {
        "owner_avatar_url": owner_avatar_url,
        "owner": owner,
        "repository": repository,
        "has_wiki": has_wiki,
        "fullname": fullname,
        "clone_url": clone_url,
        "created_at": created_at,
        "default_branch": default_branch,
        "description": description,
        "fork": fork,
        "forks_count": forks_count,
        "homepage": homepage,
        "language": language,
        "main_language": main_language,
        "name": name,
        "open_issues": open_issues,
        "pushed_at": pushed_at,
        "stargazers_count": stargazers_count,
        "updated_at": updated_at,
        "watchers_count": watchers_count,
        "subscribers_count": subscribers_count,
        "archived": archived,
        "num_files": num_files,
        "size": size,
    }
