import time

from api.lib import consts, utils

from . import querys


def get_issues(owner, repository):
    tokens = utils.get_tokens()
    issues = []
    has_next = True
    cursor = None
    while 1:
        query = querys.queryGetIssues(
            cursor, owner, repository, consts.LIMIT_QUERY_RESULT
        )
        init = time.time()
        result = utils.run_query(query, tokens)
        if not result:
            issues += result["data"]["repository"]["issues"]["nodes"]
            has_next = result["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
            cursor = result["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
            total_count = result["data"]["repository"]["issues"]["totalCount"]
            print(f"{len(issues)} de {total_count} issues recuperadas")
        print(f"Foram usados {time.time() - init} segundos")
        if not has_next:
            break

    issues = utils.parse_json(issues)

    return issues
