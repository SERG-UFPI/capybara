from script import run, returnCommits, returnIssues, returnPullRequests, returnRepository, returnRepositorys
from lib.classifiers import run as classify
from lib.get_metrics import get_all_metrics
import utils.base_model as model
import utils.response_models as response_model
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


# Insert new repository to database
@app.post('/insert', responses={200: {
    "content": {
        "application/json": {
            "example": {"success": True}
        }
    }
}})
def insert_repository(repository: model.Repository):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser inserido!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser inserido!"
            })

        owner = repository.owner
        repository = repository.repository
        run(owner, repository)
        return ({"success": True})
    except Exception as e:
        return ({"error": str(e)})


@app.get('/repositorys', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "repositorys": [
                    {
                        "owner": "ES2-UFPI",
                        "repository": "Unichat",
                        "owner_avatar_url": "https://avatars0.githubusercontent.com/u/41210541?v=4",
                        "description": "Repositório da aplicação Unichat",
                        "language": "JavaScript"
                    },
                    {
                        "owner": "d3",
                        "repository": "d3",
                        "owner_avatar_url": "https://avatars1.githubusercontent.com/u/1562726?v=4",
                        "description": "Bring data to life with SVG, Canvas and HTML. :bar_chart::chart_with_upwards_trend::tada:",
                        "language": "JavaScript"
                    }
                ]
            }
        }
    }
}})
def get_repositorys():
    try:
        repositorys = returnRepositorys()
        return ({"repositorys": repositorys})
    except Exception as e:
        return ({"error": str(e)})


@app.get('/repository/{owner}/{repository}', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "homepage": "https://d3js.org",
                "owner_avatar_url": "https://avatars1.githubusercontent.com/u/1562726?v=4",
                "stargazers_count": 92261,
                "description": "Bring data to life with SVG, Canvas and HTML. :bar_chart::chart_with_upwards_trend::tada:",
                "forks_count": 22169,
                "pushed_at": 1591322344,
                "fork": False,
                "name": "d3",
                "key": 2,
                "archived": False,
                "repository": "d3",
                "num_files": 18,
                "open_issues": 7,
                "clone_url": "https://github.com/d3/d3.git",
                "default_branch": "master",
                "main_language": "JavaScript",
                "owner": "d3",
                "subscribers_count": 3984,
                "has_wiki": True,
                "created_at": 1285618962,
                "language": "JavaScript",
                "fullname": "d3/d3",
                "size": 41514,
                "updated_at": 1593457466,
                "watchers_count": 92261
            }
        }
    }
}})
def get_repository(owner: str, repository: str):
    try:
        if owner is None or owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository is None or repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = owner
        repository_name = repository

        repository = returnRepository(owner, repository_name)
        return (repository)
    except Exception as e:
        return ({"error": str(e)})


@ app.get('/issues/{owner}/{repository}', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "totalCount": 123,
                "issues": [
                    {
                        "milestone": None,
                        "assignee": [],
                        "state": "CLOSED",
                        "comments": 4,
                        "locked": False,
                        "author": {
                            "id": "MDQ6VXNlcjEzNTc2OA==",
                            "login": "janwillemtulp",
                            "avatar_url": "https://avatars3.githubusercontent.com/u/135768?u=84c66593c6d1ced87f6dadde1e587a9cbd79bb9e&v=4",
                            "name": "Jan Willem Tulp",
                            "email": "janwillem@tulpinteractive.com",
                            "created_at": 1254845173
                        },
                        "active_lock_reason": None,
                        "id": "MDU6SXNzdWU2ODIxMzQ=",
                        "body": "Is it possible to disable an event while a transition is in progress? For instance, I have a mouseover event and a circle moves for 4000 milliseconds. Is it possible to disable the mouseover event while the circle is moving, and then re-enable the event when the transition is done?\n",
                        "title": "disabling an event while a transition is in progress?",
                        "author_association": "NONE",
                        "updated_at": 1512516387,
                        "created_at": 1300390638,
                        "closed_at": 1300738163,
                        "assignees": [],
                        "number": 77,
                        "key": 173,
                        "labels": [],
                        "reactions": []
                    }
                ]
            }
        }
    }
}})
def get_issues(owner: str, repository: str, limit: int = 0):
    try:
        if owner is None or owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository is None or repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = owner
        repository_name = repository
        limit = limit
        # pr_as_issue = pr_as_issue

        total, issues = returnIssues(owner, repository_name, limit, False)
        return ({"totalCount": total, "issues": issues})
    except Exception as e:
        return ({"error": str(e)})


@ app.get('/commits/{owner}/{repository}', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "totalCount": 123,
                "commits": [
                    {
                        "message": "Update README.md",
                        "key": 4271,
                        "merge": None,
                        "files": [
                            {
                                "modes": [
                                    "100644",
                                    "100644"
                                ],
                                "indexes": [
                                    "de6fcc6b",
                                    "8b77b620"
                                ],
                                "action": "M",
                                "file": "README.md",
                                "added": "1",
                                "removed": "1"
                            }
                        ],
                        "commiter": "Jonathan Huang <grokut@gmail.com>",
                        "commitdate": "Mon Apr 6 14:49:16 2015 -0700",
                        "signed_off_by": None,
                        "commit": "5494b5f7a1e08fca6f6015400cf0dae2f683fcfc",
                        "parents": [
                            "7355077f9dc2763732cd5cc54ca3dbd8ff89c080"
                        ],
                        "refs": [],
                        "author": "Jonathan Huang <grokut@gmail.com>",
                        "authordate": "Mon Apr 6 14:49:16 2015 -0700"
                    }
                ]
            }
        }
    }
}})
def get_commits(owner: str, repository: str, limit: int = 0):
    try:
        if owner is None or owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository is None or repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = owner
        repository_name = repository
        limit = limit

        total, commits = returnCommits(owner, repository_name, limit)
        return ({"totalCount": total, "commits": commits})
    except Exception as e:
        return ({"error": str(e)})


@ app.get('/pullrequests/{owner}/{repository}', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "totalCount": 123,
                "pull_requests": [
                    {
                        "maintainer_can_modify": False,
                        "additions": 327,
                        "commits": 1,
                        "closed_at": 1504668368,
                        "author_association": "NONE",
                        "head_ref_name": "fix-treemap",
                        "milestone": None,
                        "body": "",
                        "author": {
                            "id": "MDQ6VXNlcjMxNTI1OTk1",
                            "login": "sguib",
                            "avatar_url": "https://avatars1.githubusercontent.com/u/31525995?v=4",
                            "name": None,
                            "email": "",
                            "created_at": 1504239435
                        },
                        "locked": False,
                        "active_lock_reason": None,
                        "base_ref_name": "master",
                        "is_draft": False,
                        "created_at": 1504668316,
                        "title": "Checkpoint.",
                        "assignee": [],
                        "merged_at": None,
                        "assignees": [],
                        "number": 3139,
                        "merged_by": None,
                        "comments": 0,
                        "deletions": 162,
                        "base_repository": {
                            "id": "MDEwOlJlcG9zaXRvcnk5NDMxNDk="
                        },
                        "key": 1162,
                        "mergeable": "CONFLICTING",
                        "head_ref_oid": "9b899a519d709fc0a20ba7cdfad6a9a4a38b1d53",
                        "merged": False,
                        "changed_files": 8,
                        "url": "https://github.com/d3/d3/pull/3139",
                        "base_ref_oid": "41dad6467234c0decf68608a760e46a882d5b80e",
                        "labels": [],
                        "merge_commit": None,
                        "id": "MDExOlB1bGxSZXF1ZXN0MTM5NDQ4NDg0",
                        "state": "CLOSED",
                        "updated_at": 1504668368
                    }
                ]
            }
        }
    }
}})
def get_pull_requests(owner: str, repository: str, limit: int = 0):
    try:
        if owner is None or owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository is None or repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = owner
        repository_name = repository
        limit = limit

        total, pullrequests = returnPullRequests(owner, repository_name, limit)
        # print(pullrequests)
        return ({"totalCount": total, "pull_requests": pullrequests})
    except Exception as e:
        return ({"error": str(e)})


@ app.post('/get_metrics', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "ci": 0,
                "license": 0,
                "history": 17.333333333333332,
                "management": 0,
                "documentation": 0.3676183026984748,
                "community": 1,
                "tests": 0
            }
        }
    }
}})
def get_metrics(repository: model.Repository):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser classificado!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser classificado!"
            })

        owner = repository.owner
        repository_name = repository.repository
        metrics = get_all_metrics(owner, repository_name)
        return metrics
    except Exception as e:
        return ({"error": str(e)})


@ app.post('/classify', responses={200: {
    "content": {
        "application/json": {
            "example": {
                "valid": False
            }
        }
    }
}})
def classify_repo(repository: model.RepositoryMetrics):
    try:
        print(repository)
        saida = classify(repository.dict())
        return {"valid": saida}

    except Exception as e:
        return ({"error": str(e)})
