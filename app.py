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
      "repository": "Unichat"
    },
    {
      "owner": "d3",
      "repository": "d3"
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

@app.post('/repository', responses={200: {
    "content": {
        "application/json": {
            "example": {
    "forks_count": 22128,
    "fork": False,
    "key": 2,
    "watchers_count": 91959,
    "subscribers_count": 3983,
    "size": 41514,
    "archived": False,
    "num_files": 22,
    "homepage": "https://d3js.org",
    "owner": "d3",
    "description": "Bring data to life with SVG, Canvas and HTML. :bar_chart::chart_with_upwards_trend::tada:",
    "default_branch": "master",
    "created_at": 1285618962,
    "clone_url": "https://github.com/d3/d3.git",
    "fullname": "d3/d3",
    "repository": "d3",
    "updated_at": 1591640158,
    "stargazers_count": 91959,
    "open_issues": 6,
    "pushed_at": 1591322344,
    "name": "d3",
    "main_language": "JavaScript",
    "language": "JavaScript"
  }
        }
    }
}})
def get_repository(repository: model.Repository):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = repository.owner
        repository_name = repository.repository

        repository = returnRepository(owner, repository_name)
        return (repository)
    except Exception as e:
        return ({"error": str(e)})

@app.post('/issues', responses={200: {
    "content": {
        "application/json": {
            "example": {
  "issues": [
    {
      "assignees": [],
      "key": 227,
      "pull_request": None,
      "milestone": None,
      "reactions_data": [],
      "comments_data": [
        {
          "url": "https://api.github.com/repos/d3/d3/issues/comments/524061",
          "html_url": "https://github.com/d3/d3/issues/5#issuecomment-524061",
          "issue_url": "https://api.github.com/repos/d3/d3/issues/5",
          "id": 524061,
          "node_id": "MDEyOklzc3VlQ29tbWVudDUyNDA2MQ==",
          "user": {
            "login": "mbostock",
            "id": 230541,
            "node_id": "MDQ6VXNlcjIzMDU0MQ==",
            "avatar_url": "https://avatars2.githubusercontent.com/u/230541?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/mbostock",
            "html_url": "https://github.com/mbostock",
            "followers_url": "https://api.github.com/users/mbostock/followers",
            "following_url": "https://api.github.com/users/mbostock/following{/other_user}",
            "gists_url": "https://api.github.com/users/mbostock/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/mbostock/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/mbostock/subscriptions",
            "organizations_url": "https://api.github.com/users/mbostock/orgs",
            "repos_url": "https://api.github.com/users/mbostock/repos",
            "events_url": "https://api.github.com/users/mbostock/events{/privacy}",
            "received_events_url": "https://api.github.com/users/mbostock/received_events",
            "type": "User",
            "site_admin": False
          },
          "created_at": "2010-11-07T16:34:30Z",
          "updated_at": "2010-11-07T16:34:30Z",
          "author_association": "MEMBER",
          "body": "Done.\n",
          "reactions": {
            "url": "https://api.github.com/repos/d3/d3/issues/comments/524061/reactions",
            "total_count": 0,
            "+1": 0,
            "-1": 0,
            "laugh": 0,
            "hooray": 0,
            "confused": 0,
            "heart": 0,
            "rocket": 0,
            "eyes": 0
          },
          "user_data": {
            "login": "mbostock",
            "id": 230541,
            "node_id": "MDQ6VXNlcjIzMDU0MQ==",
            "avatar_url": "https://avatars2.githubusercontent.com/u/230541?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/mbostock",
            "html_url": "https://github.com/mbostock",
            "followers_url": "https://api.github.com/users/mbostock/followers",
            "following_url": "https://api.github.com/users/mbostock/following{/other_user}",
            "gists_url": "https://api.github.com/users/mbostock/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/mbostock/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/mbostock/subscriptions",
            "organizations_url": "https://api.github.com/users/mbostock/orgs",
            "repos_url": "https://api.github.com/users/mbostock/repos",
            "events_url": "https://api.github.com/users/mbostock/events{/privacy}",
            "received_events_url": "https://api.github.com/users/mbostock/received_events",
            "type": "User",
            "site_admin": False,
            "name": "Mike Bostock",
            "company": "@observablehq ",
            "blog": "https://bost.ocks.org/mike/",
            "location": "San Francisco, CA",
            "email": "mike@ocks.org",
            "hireable": None,
            "bio": "Building a better computational medium. Founder @observablehq. Creator @d3. Former @nytgraphics. Pronounced BOSS-tock.",
            "twitter_username": None,
            "public_repos": 65,
            "public_gists": 1043,
            "followers": 20569,
            "following": 13,
            "created_at": "2010-03-25T22:02:56Z",
            "updated_at": "2020-06-02T02:20:41Z",
            "organizations": [
              {
                "login": "protovis",
                "id": 430480,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjQzMDQ4MA==",
                "url": "https://api.github.com/orgs/protovis",
                "repos_url": "https://api.github.com/orgs/protovis/repos",
                "events_url": "https://api.github.com/orgs/protovis/events",
                "hooks_url": "https://api.github.com/orgs/protovis/hooks",
                "issues_url": "https://api.github.com/orgs/protovis/issues",
                "members_url": "https://api.github.com/orgs/protovis/members{/member}",
                "public_members_url": "https://api.github.com/orgs/protovis/public_members{/member}",
                "avatar_url": "https://avatars2.githubusercontent.com/u/430480?v=4",
                "description": ""
              },
              {
                "login": "d3",
                "id": 1562726,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjE1NjI3MjY=",
                "url": "https://api.github.com/orgs/d3",
                "repos_url": "https://api.github.com/orgs/d3/repos",
                "events_url": "https://api.github.com/orgs/d3/events",
                "hooks_url": "https://api.github.com/orgs/d3/hooks",
                "issues_url": "https://api.github.com/orgs/d3/issues",
                "members_url": "https://api.github.com/orgs/d3/members{/member}",
                "public_members_url": "https://api.github.com/orgs/d3/public_members{/member}",
                "avatar_url": "https://avatars1.githubusercontent.com/u/1562726?v=4",
                "description": "Data-Driven Documents"
              },
              {
                "login": "topojson",
                "id": 5331916,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjUzMzE5MTY=",
                "url": "https://api.github.com/orgs/topojson",
                "repos_url": "https://api.github.com/orgs/topojson/repos",
                "events_url": "https://api.github.com/orgs/topojson/events",
                "hooks_url": "https://api.github.com/orgs/topojson/hooks",
                "issues_url": "https://api.github.com/orgs/topojson/issues",
                "members_url": "https://api.github.com/orgs/topojson/members{/member}",
                "public_members_url": "https://api.github.com/orgs/topojson/public_members{/member}",
                "avatar_url": "https://avatars3.githubusercontent.com/u/5331916?v=4",
                "description": "An extension to GeoJSON that encodes topology."
              },
              {
                "login": "observablehq",
                "id": 30080011,
                "node_id": "MDEyOk9yZ2FuaXphdGlvbjMwMDgwMDEx",
                "url": "https://api.github.com/orgs/observablehq",
                "repos_url": "https://api.github.com/orgs/observablehq/repos",
                "events_url": "https://api.github.com/orgs/observablehq/events",
                "hooks_url": "https://api.github.com/orgs/observablehq/hooks",
                "issues_url": "https://api.github.com/orgs/observablehq/issues",
                "members_url": "https://api.github.com/orgs/observablehq/members{/member}",
                "public_members_url": "https://api.github.com/orgs/observablehq/public_members{/member}",
                "avatar_url": "https://avatars1.githubusercontent.com/u/30080011?v=4",
                "description": "The magic notebook for visualization."
              }
            ]
          },
          "reactions_data": []
        }
      ],
      "assignees_data": [],
      "assignee_data": {},
      "user_data": {
        "login": "mbostock",
        "id": 230541,
        "node_id": "MDQ6VXNlcjIzMDU0MQ==",
        "avatar_url": "https://avatars2.githubusercontent.com/u/230541?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/mbostock",
        "html_url": "https://github.com/mbostock",
        "followers_url": "https://api.github.com/users/mbostock/followers",
        "following_url": "https://api.github.com/users/mbostock/following{/other_user}",
        "gists_url": "https://api.github.com/users/mbostock/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/mbostock/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/mbostock/subscriptions",
        "organizations_url": "https://api.github.com/users/mbostock/orgs",
        "repos_url": "https://api.github.com/users/mbostock/repos",
        "events_url": "https://api.github.com/users/mbostock/events{/privacy}",
        "received_events_url": "https://api.github.com/users/mbostock/received_events",
        "type": "User",
        "site_admin": False,
        "name": "Mike Bostock",
        "company": "@observablehq ",
        "blog": "https://bost.ocks.org/mike/",
        "location": "San Francisco, CA",
        "email": "mike@ocks.org",
        "hireable": None,
        "bio": "Building a better computational medium. Founder @observablehq. Creator @d3. Former @nytgraphics. Pronounced BOSS-tock.",
        "twitter_username": None,
        "public_repos": 65,
        "public_gists": 1043,
        "followers": 20569,
        "following": 13,
        "created_at": "2010-03-25T22:02:56Z",
        "updated_at": "2020-06-02T02:20:41Z",
        "organizations": [
          {
            "login": "protovis",
            "id": 430480,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjQzMDQ4MA==",
            "url": "https://api.github.com/orgs/protovis",
            "repos_url": "https://api.github.com/orgs/protovis/repos",
            "events_url": "https://api.github.com/orgs/protovis/events",
            "hooks_url": "https://api.github.com/orgs/protovis/hooks",
            "issues_url": "https://api.github.com/orgs/protovis/issues",
            "members_url": "https://api.github.com/orgs/protovis/members{/member}",
            "public_members_url": "https://api.github.com/orgs/protovis/public_members{/member}",
            "avatar_url": "https://avatars2.githubusercontent.com/u/430480?v=4",
            "description": ""
          },
          {
            "login": "d3",
            "id": 1562726,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjE1NjI3MjY=",
            "url": "https://api.github.com/orgs/d3",
            "repos_url": "https://api.github.com/orgs/d3/repos",
            "events_url": "https://api.github.com/orgs/d3/events",
            "hooks_url": "https://api.github.com/orgs/d3/hooks",
            "issues_url": "https://api.github.com/orgs/d3/issues",
            "members_url": "https://api.github.com/orgs/d3/members{/member}",
            "public_members_url": "https://api.github.com/orgs/d3/public_members{/member}",
            "avatar_url": "https://avatars1.githubusercontent.com/u/1562726?v=4",
            "description": "Data-Driven Documents"
          },
          {
            "login": "topojson",
            "id": 5331916,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjUzMzE5MTY=",
            "url": "https://api.github.com/orgs/topojson",
            "repos_url": "https://api.github.com/orgs/topojson/repos",
            "events_url": "https://api.github.com/orgs/topojson/events",
            "hooks_url": "https://api.github.com/orgs/topojson/hooks",
            "issues_url": "https://api.github.com/orgs/topojson/issues",
            "members_url": "https://api.github.com/orgs/topojson/members{/member}",
            "public_members_url": "https://api.github.com/orgs/topojson/public_members{/member}",
            "avatar_url": "https://avatars3.githubusercontent.com/u/5331916?v=4",
            "description": "An extension to GeoJSON that encodes topology."
          },
          {
            "login": "observablehq",
            "id": 30080011,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjMwMDgwMDEx",
            "url": "https://api.github.com/orgs/observablehq",
            "repos_url": "https://api.github.com/orgs/observablehq/repos",
            "events_url": "https://api.github.com/orgs/observablehq/events",
            "hooks_url": "https://api.github.com/orgs/observablehq/hooks",
            "issues_url": "https://api.github.com/orgs/observablehq/issues",
            "members_url": "https://api.github.com/orgs/observablehq/members{/member}",
            "public_members_url": "https://api.github.com/orgs/observablehq/public_members{/member}",
            "avatar_url": "https://avatars1.githubusercontent.com/u/30080011?v=4",
            "description": "The magic notebook for visualization."
          }
        ]
      },
      "reactions": {
        "url": "https://api.github.com/repos/d3/d3/issues/5/reactions",
        "total_count": 0,
        "+1": 0,
        "-1": 0,
        "laugh": 0,
        "hooray": 0,
        "confused": 0,
        "heart": 0,
        "rocket": 0,
        "eyes": 0
      },
      "body": "A `sort` operator would be nice for reordering nodes.\n",
      "author_association": "MEMBER",
      "closed_at": "2010-11-07T16:34:30Z",
      "updated_at": "2010-11-07T16:34:30Z",
      "created_at": "2010-09-30T04:30:47Z",
      "locked": False,
      "assignee": None,
      "comments": 1,
      "url": "https://api.github.com/repos/d3/d3/issues/5",
      "repository_url": "https://api.github.com/repos/d3/d3",
      "labels_url": "https://api.github.com/repos/d3/d3/issues/5/labels{/name}",
      "comments_url": "https://api.github.com/repos/d3/d3/issues/5/comments",
      "events_url": "https://api.github.com/repos/d3/d3/issues/5/events",
      "html_url": "https://github.com/d3/d3/issues/5",
      "id": 340100,
      "node_id": "MDU6SXNzdWUzNDAxMDA=",
      "number": 5,
      "title": "Sorting nodes.",
      "user_info": {
        "login": "mbostock",
        "id": 230541,
        "node_id": "MDQ6VXNlcjIzMDU0MQ==",
        "avatar_url": "https://avatars2.githubusercontent.com/u/230541?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/mbostock",
        "html_url": "https://github.com/mbostock",
        "followers_url": "https://api.github.com/users/mbostock/followers",
        "following_url": "https://api.github.com/users/mbostock/following{/other_user}",
        "gists_url": "https://api.github.com/users/mbostock/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/mbostock/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/mbostock/subscriptions",
        "organizations_url": "https://api.github.com/users/mbostock/orgs",
        "repos_url": "https://api.github.com/users/mbostock/repos",
        "events_url": "https://api.github.com/users/mbostock/events{/privacy}",
        "received_events_url": "https://api.github.com/users/mbostock/received_events",
        "type": "User",
        "site_admin": False
      },
      "labels": [
        {
          "id": 50043,
          "node_id": "MDU6TGFiZWw1MDA0Mw==",
          "url": "https://api.github.com/repos/d3/d3/labels/req",
          "name": "req",
          "color": "2ca02c",
          "default": False,
          "description": None
        }
      ],
      "state": "closed"
    }
  ]
}
        }
    }
}})
def get_issues(repository: model.RepositoryLimitedIssues):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = repository.owner
        repository_name = repository.repository
        limit = repository.limit
        pr_as_issue = repository.pr_as_issue

        issues = returnIssues(owner, repository_name, limit, pr_as_issue)
        return ({"issues": issues})
    except Exception as e:
        return ({"error": str(e)})


@app.post('/commits', responses={200: {
    "content": {
        "application/json": {
            "example": {
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
def get_commits(repository: model.RepositoryLimited):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = repository.owner
        repository_name = repository.repository
        limit = repository.limit

        commits = returnCommits(owner, repository_name, limit)
        return ({"commits": commits})
    except Exception as e:
        return ({"error": str(e)})


@app.post('/pullrequests', responses={200: {
    "content": {
        "application/json": {
            "example": {
  "pull_requests": [
    {
      "labels": [],
      "merge_commit_sha": "cc7d6012ee746da89232f760b23c4fb1cff23643",
      "assignees": [],
      "requested_reviewers": [],
      "requested_teams": [],
      "draft": False,
      "commits_url": "https://api.github.com/repos/d3/d3/pulls/1651/commits",
      "review_comments_url": "https://api.github.com/repos/d3/d3/pulls/1651/comments",
      "review_comment_url": "https://api.github.com/repos/d3/d3/pulls/comments{/number}",
      "comments_url": "https://api.github.com/repos/d3/d3/issues/1651/comments",
      "statuses_url": "https://api.github.com/repos/d3/d3/statuses/4629494912705c1f6cccb626ddc99b2136398559",
      "head": {
        "label": "danielsu:i18nAtRuntime",
        "ref": "i18nAtRuntime",
        "sha": "4629494912705c1f6cccb626ddc99b2136398559",
        "user": {
          "login": "danielsu",
          "id": 3994789,
          "node_id": "MDQ6VXNlcjM5OTQ3ODk=",
          "avatar_url": "https://avatars3.githubusercontent.com/u/3994789?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/danielsu",
          "html_url": "https://github.com/danielsu",
          "followers_url": "https://api.github.com/users/danielsu/followers",
          "following_url": "https://api.github.com/users/danielsu/following{/other_user}",
          "gists_url": "https://api.github.com/users/danielsu/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/danielsu/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/danielsu/subscriptions",
          "organizations_url": "https://api.github.com/users/danielsu/orgs",
          "repos_url": "https://api.github.com/users/danielsu/repos",
          "events_url": "https://api.github.com/users/danielsu/events{/privacy}",
          "received_events_url": "https://api.github.com/users/danielsu/received_events",
          "type": "User",
          "site_admin": False
        },
        "repo": {
          "id": 14697750,
          "node_id": "MDEwOlJlcG9zaXRvcnkxNDY5Nzc1MA==",
          "name": "d3",
          "full_name": "danielsu/d3",
          "private": False,
          "owner": {
            "login": "danielsu",
            "id": 3994789,
            "node_id": "MDQ6VXNlcjM5OTQ3ODk=",
            "avatar_url": "https://avatars3.githubusercontent.com/u/3994789?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/danielsu",
            "html_url": "https://github.com/danielsu",
            "followers_url": "https://api.github.com/users/danielsu/followers",
            "following_url": "https://api.github.com/users/danielsu/following{/other_user}",
            "gists_url": "https://api.github.com/users/danielsu/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/danielsu/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/danielsu/subscriptions",
            "organizations_url": "https://api.github.com/users/danielsu/orgs",
            "repos_url": "https://api.github.com/users/danielsu/repos",
            "events_url": "https://api.github.com/users/danielsu/events{/privacy}",
            "received_events_url": "https://api.github.com/users/danielsu/received_events",
            "type": "User",
            "site_admin": False
          },
          "html_url": "https://github.com/danielsu/d3",
          "description": "A JavaScript visualization library for HTML and SVG.",
          "fork": True,
          "url": "https://api.github.com/repos/danielsu/d3",
          "forks_url": "https://api.github.com/repos/danielsu/d3/forks",
          "keys_url": "https://api.github.com/repos/danielsu/d3/keys{/key_id}",
          "collaborators_url": "https://api.github.com/repos/danielsu/d3/collaborators{/collaborator}",
          "teams_url": "https://api.github.com/repos/danielsu/d3/teams",
          "hooks_url": "https://api.github.com/repos/danielsu/d3/hooks",
          "issue_events_url": "https://api.github.com/repos/danielsu/d3/issues/events{/number}",
          "events_url": "https://api.github.com/repos/danielsu/d3/events",
          "assignees_url": "https://api.github.com/repos/danielsu/d3/assignees{/user}",
          "branches_url": "https://api.github.com/repos/danielsu/d3/branches{/branch}",
          "tags_url": "https://api.github.com/repos/danielsu/d3/tags",
          "blobs_url": "https://api.github.com/repos/danielsu/d3/git/blobs{/sha}",
          "git_tags_url": "https://api.github.com/repos/danielsu/d3/git/tags{/sha}",
          "git_refs_url": "https://api.github.com/repos/danielsu/d3/git/refs{/sha}",
          "trees_url": "https://api.github.com/repos/danielsu/d3/git/trees{/sha}",
          "statuses_url": "https://api.github.com/repos/danielsu/d3/statuses/{sha}",
          "languages_url": "https://api.github.com/repos/danielsu/d3/languages",
          "stargazers_url": "https://api.github.com/repos/danielsu/d3/stargazers",
          "contributors_url": "https://api.github.com/repos/danielsu/d3/contributors",
          "subscribers_url": "https://api.github.com/repos/danielsu/d3/subscribers",
          "subscription_url": "https://api.github.com/repos/danielsu/d3/subscription",
          "commits_url": "https://api.github.com/repos/danielsu/d3/commits{/sha}",
          "git_commits_url": "https://api.github.com/repos/danielsu/d3/git/commits{/sha}",
          "comments_url": "https://api.github.com/repos/danielsu/d3/comments{/number}",
          "issue_comment_url": "https://api.github.com/repos/danielsu/d3/issues/comments{/number}",
          "contents_url": "https://api.github.com/repos/danielsu/d3/contents/{+path}",
          "compare_url": "https://api.github.com/repos/danielsu/d3/compare/{base}...{head}",
          "merges_url": "https://api.github.com/repos/danielsu/d3/merges",
          "archive_url": "https://api.github.com/repos/danielsu/d3/{archive_format}{/ref}",
          "downloads_url": "https://api.github.com/repos/danielsu/d3/downloads",
          "issues_url": "https://api.github.com/repos/danielsu/d3/issues{/number}",
          "pulls_url": "https://api.github.com/repos/danielsu/d3/pulls{/number}",
          "milestones_url": "https://api.github.com/repos/danielsu/d3/milestones{/number}",
          "notifications_url": "https://api.github.com/repos/danielsu/d3/notifications{?since,all,participating}",
          "labels_url": "https://api.github.com/repos/danielsu/d3/labels{/name}",
          "releases_url": "https://api.github.com/repos/danielsu/d3/releases{/id}",
          "deployments_url": "https://api.github.com/repos/danielsu/d3/deployments",
          "created_at": "2013-11-25T20:39:49Z",
          "updated_at": "2016-05-13T16:00:03Z",
          "pushed_at": "2013-11-29T09:38:31Z",
          "git_url": "git://github.com/danielsu/d3.git",
          "ssh_url": "git@github.com:danielsu/d3.git",
          "clone_url": "https://github.com/danielsu/d3.git",
          "svn_url": "https://github.com/danielsu/d3",
          "homepage": "http://d3js.org",
          "size": 27625,
          "stargazers_count": 0,
          "watchers_count": 0,
          "language": "JavaScript",
          "has_issues": False,
          "has_projects": True,
          "has_downloads": True,
          "has_wiki": True,
          "has_pages": False,
          "forks_count": 0,
          "mirror_url": None,
          "archived": False,
          "disabled": False,
          "open_issues_count": 0,
          "license": {
            "key": "other",
            "name": "Other",
            "spdx_id": "NOASSERTION",
            "url": None,
            "node_id": "MDc6TGljZW5zZTA="
          },
          "forks": 0,
          "open_issues": 0,
          "watchers": 0,
          "default_branch": "master"
        }
      },
      "base": {
        "label": "mbostock:master",
        "ref": "master",
        "sha": "525cbbfee88d5203abb7b19592046431079c3d81",
        "user": {
          "login": "mbostock",
          "id": 230541,
          "node_id": "MDQ6VXNlcjIzMDU0MQ==",
          "avatar_url": "https://avatars2.githubusercontent.com/u/230541?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/mbostock",
          "html_url": "https://github.com/mbostock",
          "followers_url": "https://api.github.com/users/mbostock/followers",
          "following_url": "https://api.github.com/users/mbostock/following{/other_user}",
          "gists_url": "https://api.github.com/users/mbostock/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/mbostock/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/mbostock/subscriptions",
          "organizations_url": "https://api.github.com/users/mbostock/orgs",
          "repos_url": "https://api.github.com/users/mbostock/repos",
          "events_url": "https://api.github.com/users/mbostock/events{/privacy}",
          "received_events_url": "https://api.github.com/users/mbostock/received_events",
          "type": "User",
          "site_admin": False
        },
        "repo": {
          "id": 943149,
          "node_id": "MDEwOlJlcG9zaXRvcnk5NDMxNDk=",
          "name": "d3",
          "full_name": "d3/d3",
          "private": False,
          "owner": {
            "login": "d3",
            "id": 1562726,
            "node_id": "MDEyOk9yZ2FuaXphdGlvbjE1NjI3MjY=",
            "avatar_url": "https://avatars1.githubusercontent.com/u/1562726?v=4",
            "gravatar_id": "",
            "url": "https://api.github.com/users/d3",
            "html_url": "https://github.com/d3",
            "followers_url": "https://api.github.com/users/d3/followers",
            "following_url": "https://api.github.com/users/d3/following{/other_user}",
            "gists_url": "https://api.github.com/users/d3/gists{/gist_id}",
            "starred_url": "https://api.github.com/users/d3/starred{/owner}{/repo}",
            "subscriptions_url": "https://api.github.com/users/d3/subscriptions",
            "organizations_url": "https://api.github.com/users/d3/orgs",
            "repos_url": "https://api.github.com/users/d3/repos",
            "events_url": "https://api.github.com/users/d3/events{/privacy}",
            "received_events_url": "https://api.github.com/users/d3/received_events",
            "type": "Organization",
            "site_admin": False
          },
          "html_url": "https://github.com/d3/d3",
          "description": "Bring data to life with SVG, Canvas and HTML. :bar_chart::chart_with_upwards_trend::tada:",
          "fork": False,
          "url": "https://api.github.com/repos/d3/d3",
          "forks_url": "https://api.github.com/repos/d3/d3/forks",
          "keys_url": "https://api.github.com/repos/d3/d3/keys{/key_id}",
          "collaborators_url": "https://api.github.com/repos/d3/d3/collaborators{/collaborator}",
          "teams_url": "https://api.github.com/repos/d3/d3/teams",
          "hooks_url": "https://api.github.com/repos/d3/d3/hooks",
          "issue_events_url": "https://api.github.com/repos/d3/d3/issues/events{/number}",
          "events_url": "https://api.github.com/repos/d3/d3/events",
          "assignees_url": "https://api.github.com/repos/d3/d3/assignees{/user}",
          "branches_url": "https://api.github.com/repos/d3/d3/branches{/branch}",
          "tags_url": "https://api.github.com/repos/d3/d3/tags",
          "blobs_url": "https://api.github.com/repos/d3/d3/git/blobs{/sha}",
          "git_tags_url": "https://api.github.com/repos/d3/d3/git/tags{/sha}",
          "git_refs_url": "https://api.github.com/repos/d3/d3/git/refs{/sha}",
          "trees_url": "https://api.github.com/repos/d3/d3/git/trees{/sha}",
          "statuses_url": "https://api.github.com/repos/d3/d3/statuses/{sha}",
          "languages_url": "https://api.github.com/repos/d3/d3/languages",
          "stargazers_url": "https://api.github.com/repos/d3/d3/stargazers",
          "contributors_url": "https://api.github.com/repos/d3/d3/contributors",
          "subscribers_url": "https://api.github.com/repos/d3/d3/subscribers",
          "subscription_url": "https://api.github.com/repos/d3/d3/subscription",
          "commits_url": "https://api.github.com/repos/d3/d3/commits{/sha}",
          "git_commits_url": "https://api.github.com/repos/d3/d3/git/commits{/sha}",
          "comments_url": "https://api.github.com/repos/d3/d3/comments{/number}",
          "issue_comment_url": "https://api.github.com/repos/d3/d3/issues/comments{/number}",
          "contents_url": "https://api.github.com/repos/d3/d3/contents/{+path}",
          "compare_url": "https://api.github.com/repos/d3/d3/compare/{base}...{head}",
          "merges_url": "https://api.github.com/repos/d3/d3/merges",
          "archive_url": "https://api.github.com/repos/d3/d3/{archive_format}{/ref}",
          "downloads_url": "https://api.github.com/repos/d3/d3/downloads",
          "issues_url": "https://api.github.com/repos/d3/d3/issues{/number}",
          "pulls_url": "https://api.github.com/repos/d3/d3/pulls{/number}",
          "milestones_url": "https://api.github.com/repos/d3/d3/milestones{/number}",
          "notifications_url": "https://api.github.com/repos/d3/d3/notifications{?since,all,participating}",
          "labels_url": "https://api.github.com/repos/d3/d3/labels{/name}",
          "releases_url": "https://api.github.com/repos/d3/d3/releases{/id}",
          "deployments_url": "https://api.github.com/repos/d3/d3/deployments",
          "created_at": "2010-09-27T17:22:42Z",
          "updated_at": "2020-06-08T15:15:58Z",
          "pushed_at": "2020-06-04T22:59:04Z",
          "git_url": "git://github.com/d3/d3.git",
          "ssh_url": "git@github.com:d3/d3.git",
          "clone_url": "https://github.com/d3/d3.git",
          "svn_url": "https://github.com/d3/d3",
          "homepage": "https://d3js.org",
          "size": 41514,
          "stargazers_count": 91959,
          "watchers_count": 91959,
          "language": "JavaScript",
          "has_issues": True,
          "has_projects": False,
          "has_downloads": True,
          "has_wiki": True,
          "has_pages": False,
          "forks_count": 22129,
          "mirror_url": None,
          "archived": False,
          "disabled": False,
          "open_issues_count": 6,
          "license": {
            "key": "bsd-3-clause",
            "name": "BSD 3-Clause \"New\" or \"Revised\" License",
            "spdx_id": "BSD-3-Clause",
            "url": "https://api.github.com/licenses/bsd-3-clause",
            "node_id": "MDc6TGljZW5zZTU="
          },
          "forks": 22129,
          "open_issues": 6,
          "watchers": 91959,
          "default_branch": "master"
        }
      },
      "_links": {
        "self": {
          "href": "https://api.github.com/repos/d3/d3/pulls/1651"
        },
        "html": {
          "href": "https://github.com/d3/d3/pull/1651"
        },
        "issue": {
          "href": "https://api.github.com/repos/d3/d3/issues/1651"
        },
        "comments": {
          "href": "https://api.github.com/repos/d3/d3/issues/1651/comments"
        },
        "review_comments": {
          "href": "https://api.github.com/repos/d3/d3/pulls/1651/comments"
        },
        "review_comment": {
          "href": "https://api.github.com/repos/d3/d3/pulls/comments{/number}"
        },
        "commits": {
          "href": "https://api.github.com/repos/d3/d3/pulls/1651/commits"
        },
        "statuses": {
          "href": "https://api.github.com/repos/d3/d3/statuses/4629494912705c1f6cccb626ddc99b2136398559"
        }
      },
      "author_association": "NONE",
      "merged": False,
      "mergeable_state": "unknown",
      "merged_by": None,
      "comments": 1,
      "review_comments": 0,
      "maintainer_can_modify": False,
      "commits": 3,
      "additions": 60,
      "deletions": 7,
      "changed_files": 3,
      "user_data": {
        "login": "danielsu",
        "id": 3994789,
        "node_id": "MDQ6VXNlcjM5OTQ3ODk=",
        "avatar_url": "https://avatars3.githubusercontent.com/u/3994789?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/danielsu",
        "html_url": "https://github.com/danielsu",
        "followers_url": "https://api.github.com/users/danielsu/followers",
        "following_url": "https://api.github.com/users/danielsu/following{/other_user}",
        "gists_url": "https://api.github.com/users/danielsu/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/danielsu/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/danielsu/subscriptions",
        "organizations_url": "https://api.github.com/users/danielsu/orgs",
        "repos_url": "https://api.github.com/users/danielsu/repos",
        "events_url": "https://api.github.com/users/danielsu/events{/privacy}",
        "received_events_url": "https://api.github.com/users/danielsu/received_events",
        "type": "User",
        "site_admin": False,
        "name": "Daniel Süß / Suess",
        "company": None,
        "blog": "",
        "location": "Berlin, Germany",
        "email": None,
        "hireable": None,
        "bio": None,
        "twitter_username": None,
        "public_repos": 7,
        "public_gists": 0,
        "followers": 0,
        "following": 0,
        "created_at": "2013-03-28T10:40:03Z",
        "updated_at": "2020-02-18T21:17:17Z",
        "organizations": []
      },
      "review_comments_data": {},
      "reviews_data": [],
      "requested_reviewers_data": [],
      "merged_by_data": [],
      "commits_data": [
        "b42592a5074bf50ed9af8fc9161506c057ed9d40",
        "b80320f5ea40fd7bb7be3af89f106faf2c44be82",
        "4629494912705c1f6cccb626ddc99b2136398559"
      ],
      "assignee": None,
      "mergeable": None,
      "rebaseable": None,
      "milestone": None,
      "key": 106,
      "url": "https://api.github.com/repos/d3/d3/pulls/1651",
      "id": 10390583,
      "node_id": "MDExOlB1bGxSZXF1ZXN0MTAzOTA1ODM=",
      "html_url": "https://github.com/d3/d3/pull/1651",
      "diff_url": "https://github.com/d3/d3/pull/1651.diff",
      "patch_url": "https://github.com/d3/d3/pull/1651.patch",
      "issue_url": "https://api.github.com/repos/d3/d3/issues/1651",
      "number": 1651,
      "state": "closed",
      "locked": False,
      "title": "I18n (internationalization and localization) at runtime",
      "user_info": {
        "login": "danielsu",
        "id": 3994789,
        "node_id": "MDQ6VXNlcjM5OTQ3ODk=",
        "avatar_url": "https://avatars3.githubusercontent.com/u/3994789?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/danielsu",
        "html_url": "https://github.com/danielsu",
        "followers_url": "https://api.github.com/users/danielsu/followers",
        "following_url": "https://api.github.com/users/danielsu/following{/other_user}",
        "gists_url": "https://api.github.com/users/danielsu/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/danielsu/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/danielsu/subscriptions",
        "organizations_url": "https://api.github.com/users/danielsu/orgs",
        "repos_url": "https://api.github.com/users/danielsu/repos",
        "events_url": "https://api.github.com/users/danielsu/events{/privacy}",
        "received_events_url": "https://api.github.com/users/danielsu/received_events",
        "type": "User",
        "site_admin": False
      },
      "body": "Dear Mike Bostock,\nout of the box D3.js is shipped with english text labels for months and week names.\nSetting axis-date-format is already possible and I can differ the format depending on the language.\nI like to add the option to do so for labels, too.\nIn my WebApp users can select their favourite language.\nBut I do not like to store multiple D3 files, differing only at a few rows of string definitions.\nWith this patch, you could overwrite the labels to any language you like.\n As far as I know, renaming this strings later does not produce side effects, because calculations e. g. european and us calendar weeks are already done.\n\n1) import d3.js\n2) set localised strings like\nswitch ( locale ) {\n            case 'de':\n                d3.time.setLocalizedStrings( MyLocalizations.localeStrings.de.dayNames,\n                        MyLocalizations.localeStrings.de.dayNamesShort,\n                        MyLocalizations.localeStrings.de.monthNames,\n                        MyLocalizations.localeStrings.de.monthNamesShort );\n                // localizeD3DateFormat: use german presets\n                break;\n            case 'fr':\n                d3.time.setLocalizedStrings( MyLocalizations.localeStrings.fr.dayNames,\n                        MyLocalizations.localeStrings.fr.dayNamesShort,\n                        MyLocalizations.localeStrings.fr.monthNames,\n                        MyLocalizations.localeStrings.fr.monthNamesShort );\n                break;\n            case 'en': ...........\n3) start using d3\n\nSo it is possible to rewrite the labels to any language you like without shipping multiple files of almost the same content.\nIs there a better way to do so?\nWhat is your oppinion?\n\nKind regards,\nDaniel Suess from Berlin\n",
      "created_at": "2013-11-29T10:06:14Z",
      "updated_at": "2014-06-12T04:37:40Z",
      "closed_at": "2013-11-29T16:26:08Z",
      "merged_at": None
    }
  ]
}
        }
    }
}})
def get_pull_requests(repository: model.RepositoryLimited):
    try:
        if repository.owner is None or repository.owner == "":
            return ({
                "error":
                "É necessário que seja informado no body o dono do repositório a ser recuperado!"
            })
        if repository.repository is None or repository.repository == "":
            return ({
                "error":
                "É necessário que seja informado no body o nome do repositório a ser recuperado!"
            })

        owner = repository.owner
        repository_name = repository.repository
        limit = repository.limit

        pullrequests = returnPullRequests(owner, repository_name, limit)
        # print(pullrequests)
        return ({"pull_requests": pullrequests})
    except Exception as e:
        return ({"error": str(e)})


@app.post('/get_metrics', responses={200: {
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


@app.post('/classify', responses={200: {
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
