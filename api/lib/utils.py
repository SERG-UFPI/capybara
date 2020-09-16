import datetime
import os
import re
import time
from pathlib import Path

import pydotenv
import requests
from github import Github
from pygount import ProjectSummary, SourceAnalysis

from api.lib import consts

global _numFiles

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = pydotenv.Environment()


def get_best_token():
    tokens = get_tokens()
    token_with_greatest_rate_limiting = None
    greatest_rate_limiting = -1
    for token in tokens:
        g_temp = Github(token)
        try:
            rate_limiting = g_temp.rate_limiting[0]
            if rate_limiting is None and rate_limiting > greatest_rate_limiting:
                greatest_rate_limiting = rate_limiting
                token_with_greatest_rate_limiting = token
        except Exception:
            continue

    return token_with_greatest_rate_limiting


def get_tokens():
    return [
        ENV.get(f"TOKEN_{x}") for x in range(1, 9999) if ENV.get(f"TOKEN_{x}", None)
    ]


def getNumFilesAux(path):
    global _numFiles
    contents = os.listdir(path)

    for content in contents:
        content_path = path + "/" + content

        if os.path.isdir(content_path):
            if content == ".git":
                continue
            else:
                getNumFilesAux(content_path)
        else:
            _numFiles += 1


def getNumFiles(owner, repository):
    global _numFiles
    _numFiles = 0
    # print(f"BASE DIR ====> {BASE_DIR}")
    getNumFilesAux(f"{BASE_DIR}/cloned_repositories/{owner}/{repository}")
    return _numFiles


def run_query(query, tokens):
    list_tokens = tokens

    for token in list_tokens[:]:
        try:
            _header = {"Authorization": f"Bearer {token}"}
            request = requests.post(
                consts.BASE_URL, json={"query": query}, headers=_header
            )

            if request.status_code == 200:
                return request.json()
            else:
                raise Exception(
                    f'Query failed to run by returning code of {request.status_code}\nMessage: "{request.content}"'
                )
        except Exception as e:
            print(e)
            list_tokens.insert(-1, list_tokens.pop())
            continue


def parseJson(file):
    newList = []
    for item in file:
        newList.append(parseJsonAux(item))
    return newList


def parseJsonAux(item):
    newDict = {}
    for key in item.keys():
        cc_key = key
        # print(f"====> item[{key}] ({item[key]}) is a {type(item[key])}")
        if type(item[key]) is dict:
            # print(f"====> item[{key}] ({item[key]}) is a dict")
            if list(item[key].keys()).count("nodes") > 0:
                newDict[cc_key] = []
                for i in item[key]["nodes"]:
                    newDict[cc_key].append(parseJsonAux(i))
            elif list(item[key].keys()).count("totalCount") > 0:
                newDict[cc_key] = item[key]["totalCount"]
            else:
                newDict[cc_key] = parseJsonAux(item[key])
        else:
            if cc_key.find("At") != -1:
                newDict[cc_key] = toTimestamp(item[key])
            else:
                newDict[cc_key] = item[key]
    return newDict


def toDate(timestamp):
    return (
        None
        if timestamp is None
        else time.strftime(
            "%a %d %b %Y %H:%M:%S GMT", time.gmtime(float(timestamp) / 1000.0)
        )
    )


def toTimestamp(date):
    return (
        None
        if date is None
        else time.mktime(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").timetuple()
        )
    )


def camelToSnake(s):
    _underscorer1 = re.compile(r"(.)([A-Z][a-z]+)")
    _underscorer2 = re.compile("([a-z0-9])([A-Z])")
    subbed = _underscorer1.sub(r"\1_\2", s)
    return _underscorer2.sub(r"\1_\2", subbed).lower()


def toCamelCase(snake_str):
    str = camelToSnake(snake_str)
    components = str.split("_")
    if len(components) < 1:
        return components
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
    return components[0].lower() + "".join(x.title() for x in components[1:])


def counterProject(path):
    """
    Returns:
        - Sum of code lines
        - Sum of documentation lines
        - Sum of empty lines
    """
    ps = ProjectSummary()

    source_paths = None

    if os.path.isdir(path):
        source_paths = getListOfFiles(path)
    else:
        source_paths = [path]

    for source_path in source_paths:
        try:
            sa = SourceAnalysis.from_file(source_path, "pygount")
            ps.add(sa)
        except Exception as e:
            # print(f'Error on analysis file: {source_path} => {e}')
            continue

    sum_code = 0
    sum_documentation = 0
    sum_empty = 0
    for ls in ps.language_to_language_summary_map.values():
        sum_code += ls.code_count
        sum_documentation += ls.documentation_count
        sum_empty += ls.empty_count

    return sum_code, sum_documentation, sum_empty


def getListOfFiles(dirName):
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}
