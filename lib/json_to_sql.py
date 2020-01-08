from lib.create_script import createTableScript, createRelationshipCommitsRepositorysScript, createRelationshipIssuesRepositorysScript, createRelationshipPullRequestsRepositorysScript
from lib.alter_script import alterTableScript


def jsonToSql(connection, tables, repository):
    print("PARSING TO SQL...")
    cursor = connection.cursor()

    owner_name = repository["repository"][0]["data"]["owner"]
    repository_name = repository["repository"][0]["data"]["repository"]
