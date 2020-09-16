import time

from api.lib import consts, utils

from . import querys


def getPullrequests(owner, repository):
    tokens = utils.get_tokens()
    pullrequests = []
    hasNext = True
    cursor = None
    while 1:
        q = querys.queryGetPullRequests(
            cursor, owner, repository, consts.LIMIT_QUERY_RESULT
        )
        init = time.time()
        result = utils.run_query(q, tokens)
        if not result:
            pullrequests += result["data"]["repository"]["pullRequests"]["nodes"]
            hasNext = result["data"]["repository"]["pullRequests"]["pageInfo"][
                "hasNextPage"
            ]
            cursor = result["data"]["repository"]["pullRequests"]["pageInfo"][
                "endCursor"
            ]
            totalCount = result["data"]["repository"]["pullRequests"]["totalCount"]
            print(f"{len(pullrequests)} de {totalCount} pullRequests recuperadas")
        print(f"Foram usados {time.time() - init} segundos")
        if not hasNext:
            break

    pullrequests = utils.parseJson(pullrequests)

    return pullrequests
