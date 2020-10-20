from pathlib import Path
import datetime
import zipfile
import os
import re
import time

import pydotenv
import requests
from github import Github, RateLimitExceededException
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
        except RateLimitExceededException:
            continue

    return token_with_greatest_rate_limiting


def get_tokens():
    return [
        ENV.get(f"TOKEN_{x}") for x in range(1, 9999) if ENV.get(f"TOKEN_{x}", None)
    ]


def get_num_files_aux(path):
    global _numFiles
    contents = os.listdir(path)

    for content in contents:
        content_path = path + "/" + content

        if os.path.isdir(content_path):
            if content == ".git":
                continue
            else:
                get_num_files_aux(content_path)
        else:
            _numFiles += 1


def get_num_files(owner, repository):
    global _numFiles
    _dir = f"{BASE_DIR}/cloned_repositories/{owner}/{repository}"

    if os.path.exists(_dir):
        _numFiles = 0
        get_num_files_aux(_dir)
        return _numFiles

    return None


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

            raise Exception(
                f'Query failed to run by returning code of {request.status_code}\nMessage: "{request.content}"'
            )
        except Exception as error:
            print(error)
            list_tokens.insert(-1, list_tokens.pop())
            continue


def parse_json(file):
    new_list = []
    for item in file:
        new_list.append(parse_json_aux(item))
    return new_list


def parse_json_aux(item):
    new_dict = {}
    for key in item.keys():
        cc_key = key
        # print(f"====> item[{key}] ({item[key]}) is a {type(item[key])}")
        if type(item[key]) is dict:
            # print(f"====> item[{key}] ({item[key]}) is a dict")
            if list(item[key].keys()).count("nodes") > 0:
                new_dict[cc_key] = []
                for i in item[key]["nodes"]:
                    new_dict[cc_key].append(parse_json_aux(i))
            elif list(item[key].keys()).count("totalCount") > 0:
                new_dict[cc_key] = item[key]["totalCount"]
            else:
                new_dict[cc_key] = parse_json_aux(item[key])
        else:
            if cc_key.find("At") != -1:
                new_dict[cc_key] = to_timestamp(item[key])
            else:
                new_dict[cc_key] = item[key]
    return new_dict


def to_date(timestamp):
    return (
        None
        if timestamp is None
        else time.strftime(
            "%a %d %b %Y %H:%M:%S GMT", time.gmtime(float(timestamp) / 1000.0)
        )
    )


def to_timestamp(date):
    return (
        None
        if date is None
        else time.mktime(
            datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ").timetuple()
        )
    )


def camel_to_snake(str):
    _underscorer1 = re.compile(r"(.)([A-Z][a-z]+)")
    _underscorer2 = re.compile("([a-z0-9])([A-Z])")
    subbed = _underscorer1.sub(r"\1_\2", str)
    return _underscorer2.sub(r"\1_\2", subbed).lower()


def to_camel_case(snake_str):
    str = camel_to_snake(snake_str)
    components = str.split("_")
    if len(components) < 1:
        return components
        # We capitalize the first letter of each component except the first one
        # with the 'title' method and join them together.
    return components[0].lower() + "".join(x.title() for x in components[1:])


def counter_project(path):
    """
    Returns:
        - Sum of code lines
        - Sum of documentation lines
        - Sum of empty lines
    """
    project_summary = ProjectSummary()

    source_paths = None

    if os.path.isdir(path):
        source_paths = get_list_of_files(path)
    else:
        source_paths = [path]

    for source_path in source_paths:
        try:
            source_analysis = SourceAnalysis.from_file(source_path, "pygount")
            project_summary.add(source_analysis)
        except Exception as error:
            # print(f'Error on analysis file: {source_path} => {e}')
            continue

    sum_code = 0
    sum_documentation = 0
    sum_empty = 0
    for language_summary in project_summary.language_to_language_summary_map.values():
        sum_code += language_summary.code_count
        sum_documentation += language_summary.documentation_count
        sum_empty += language_summary.empty_count

    return sum_code, sum_documentation, sum_empty


def get_list_of_files(dir_name):
    list_of_files = os.listdir(dir_name)
    all_files = list()
    # Iterate over all the entries
    for entry in list_of_files:
        # Create full path
        full_path = os.path.join(dir_name, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(full_path):
            all_files = all_files + get_list_of_files(full_path)
        else:
            all_files.append(full_path)

    return all_files


def without_keys(dictionary, keys):
    return {x: dictionary[x] for x in dictionary if x not in keys}


def zipdir(path, filename):
    zipf = zipfile.ZipFile(f"{filename}.zip", "w", zipfile.ZIP_DEFLATED)

    for dir_, _, files in os.walk(f"{BASE_DIR}/{path}"):
        for file_name in files:
            rel_dir = os.path.relpath(dir_, f"{BASE_DIR}/{path}")
            try:
                zipf.write(os.path.join(f"./{path}/" + rel_dir, file_name))
            except Exception as error:
                print(error)

    zipf.close()
