import time

from api.lib import consts, utils

from . import querys


def get_pullrequests(owner, repository):
    tokens = utils.get_tokens()
    pullrequests = []
    has_next = True
    cursor = None
    while 1:
        query = querys.query_get_pullrequests(
            cursor, owner, repository, consts.LIMIT_QUERY_RESULT
        )
        init = time.time()
        result = utils.run_query(query, tokens)
        if result:
            pullrequests += result["data"]["repository"]["pullRequests"]["nodes"]
            has_next = result["data"]["repository"]["pullRequests"]["pageInfo"][
                "hasNextPage"
            ]
            cursor = result["data"]["repository"]["pullRequests"]["pageInfo"][
                "endCursor"
            ]
            total_count = result["data"]["repository"]["pullRequests"]["totalCount"]
            print(f"{len(pullrequests)} de {total_count} pullRequests recuperadas")
        print(f"Foram usados {time.time() - init} segundos")
        if not has_next:
            break

    pullrequests = utils.parse_json(pullrequests)

    return pullrequests
