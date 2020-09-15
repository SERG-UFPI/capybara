from api.lib import consts, utils
from . import querys
import time


def getIssues(owner, repository):
    tokens = utils.get_tokens()
    issues = []
    hasNext = True
    cursor = None
    while 1:
        query = querys.queryGetIssues(
            cursor, owner, repository, consts.LIMIT_QUERY_RESULT)
        init = time.time()
        result = utils.run_query(query, tokens)
        if not result is None:
            issues += result["data"]["repository"]["issues"]["nodes"]
            hasNext = result["data"]["repository"]["issues"]["pageInfo"]["hasNextPage"]
            cursor = result["data"]["repository"]["issues"]["pageInfo"]["endCursor"]
            totalCount = result["data"]["repository"]["issues"]["totalCount"]
            print(
                f"{len(issues)} de {totalCount} issues recuperadas")
        print(
            f"Foram usados {time.time() - init} segundos")
        if (not hasNext):
            break

    issues = utils.parseJson(issues)

    return issues
