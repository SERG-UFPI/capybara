from git_retriever.querys import queryGetPullRequests, queryGetIssues
from git_retriever.utils import camelToSnake
from typing import Dict, List
from github import Github
import requests
import datetime
import json
import time
import os
# from python_graphql_client import GraphqlClient


def toTimestamp(date):
    return None if date is None else time.mktime(datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").timetuple())


class GithubRetriever():
    def __init__(self, tokens=[], limit_query=100):
        # self.client = GraphqlClient(
        #     endpoint="https://api.github.com/graphql")
        self.tokens = tokens
        self.BASE_URL = "https://api.github.com/graphql"
        self.limit_query = limit_query

    def run_query(self, query):
        for token in self.tokens[:]:
            try:
                _header = {"Authorization": f"Bearer {token}"}
                request = requests.post(self.BASE_URL, json={
                                        'query': query}, headers=_header)
                # result = self.client.execute(query=query, headers=_header)
                # return result
                if request.status_code == 200:
                    return request.json()
                else:
                    raise Exception(
                        f"Query failed to run by returning code of {request.status_code}\nMessage: \"{request.content}\"")
            except Exception as e:
                print(e)
                self.tokens.insert(-1, self.tokens.pop())
                continue

    def retrieve_pullrequests(self, owner, repository):
        pullrequests = []
        hasNext = True
        cursor = None
        while 1:
            q = queryGetPullRequests(
                cursor, owner, repository, self.limit_query)
            init = time.time()
            result = self.run_query(q)
            if not result is None:
                pullrequests += result["data"]["repository"]["pullRequests"]["nodes"]
                hasNext = result["data"]["repository"]["pullRequests"]["pageInfo"]["hasNextPage"]
                cursor = result["data"]["repository"]["pullRequests"]["pageInfo"]["endCursor"]
                totalCount = result["data"]["repository"]["pullRequests"]["totalCount"]
                print(
                    f"{len(pullrequests)} de {totalCount} pullRequests recuperadas")
            print(
                f"Foram usados {time.time() - init} segundos")
            if (not hasNext):
                break

        pullrequests = self.parseJson(pullrequests)

        return pullrequests

    def retrieve_issues(self, owner, repository):
        issues = []
        hasNext = True
        cursor = None
        while 1:
            q = queryGetIssues(cursor, owner, repository, self.limit_query)
            init = time.time()
            result = self.run_query(q)
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

        issues = self.parseJson(issues)

        return issues

    def parseJson(self, file):
        newList = []
        for item in file:
            newList.append(self.parseJsonAux(item))
        return newList

    def parseJsonAux(self, item: Dict) -> Dict:
        newDict = {}
        for key in item.keys():
            cc_key = camelToSnake(key)
            # print(f"====> item[{key}] ({item[key]}) is a {type(item[key])}")
            if type(item[key]) is dict:
                # print(f"====> item[{key}] ({item[key]}) is a dict")
                if list(item[key].keys()).count("nodes") > 0:
                    newDict[cc_key] = []
                    for i in item[key]["nodes"]:
                        newDict[cc_key].append(self.parseJsonAux(i))
                elif list(item[key].keys()).count("totalCount") > 0:
                    newDict[cc_key] = item[key]["totalCount"]
                else:
                    newDict[cc_key] = self.parseJsonAux(item[key])
            else:
                if cc_key.find("_at") != -1:
                    newDict[cc_key] = toTimestamp(item[key])
                else:
                    newDict[cc_key] = item[key]
        return newDict


if __name__ == "__main__":
    owner = "d3"
    repository = "d3"
    tokens = []

    index = 1

    while 1:
        token = os.environ.get(f"TOKEN_{index}")
        if token != None:
            tokens.append(token)
            index += 1
        else:
            break

    # Initialize github retriever
    gr = GithubRetriever(tokens=tokens)

    # print("Retrieving issues!")
    # init = time.time()
    # issues = gr.retrieve_issues(owner=owner, repository=repository)
    # print(f"Tempo total: {(time.time() - init)/60} minutos")
    # print("Completed!")
    # print(f"{len(issues)} issues retrieved")
    # print("Writing issues!")
    # file = open(f"issues_{owner}_{repository}.json", "w")
    # file.write(json.dumps(issues))
    # file.close()
    # print("Issues writed.")
    # print("================================================================")

    print("Retrieving pullrequests!")
    init = time.time()
    pullrequests = gr.retrieve_pullrequests(
        owner=owner, repository=repository)
    print(f"Tempo total: {(time.time() - init)/60} minutos")
    print("Completed!")
    print(f"{len(pullrequests)} pullrequests retrieved")
    print("Writing PullRequests!")
    file = open(f"pullrequests_{owner}_{repository}.json", "w")
    file.write(json.dumps(pullrequests))
    file.close()
    print("PullRequests writed.")
    print("================================================================")
