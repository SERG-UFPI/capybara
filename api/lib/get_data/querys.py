def user_info_query():
    return """
        id
        login
        avatarUrl
        # isSiteAdmin
        name
        # company
        # websiteUrl
        # location
        email
        # isHireable
        # bio
        # twitterUsername
        # repositories {
        #   totalDiskUsage
        #   totalCount
        # }
        # followers {
        #   totalCount
        # }
        # following {
        #   totalCount
        # }
        createdAt
        # updatedAt
        # contributionsCollection {
        #   totalPullRequestReviewContributions
        # }
        # organizations {
        #  totalCount
        # }"""


def label_info_query():
    return """
        color
        description
        name
        url"""


def milestone_info_query():
    return """
      closed
      closedAt
      createdAt
      creator {
        avatarUrl
        login
      }
      description
      dueOn
      id
      number
      issues(states: OPEN) {
        totalCount
      }
      state
      title
      updatedAt
      url"""


def query_get_pullrequests(cursor, owner, repository, limit):
    _cursor = "null" if cursor is None else ('"' + cursor + '"')
    return f"""
{{
  repository(owner: "{owner}", name: "{repository}") {{
    pullRequests(first: {80}, after: {_cursor}) {{
        totalCount
        nodes {{
          activeLockReason
          additions
          assignee: assignees (first: 1) {{
            nodes {{{user_info_query()}
            }}
          }}
          assignees (first: 10) {{
            nodes {{{user_info_query()}
            }}
          }} 
          authorAssociation
          baseRefOid
          baseRefName
          baseRepository {{
            id
          }}
          body
          changedFiles
          closedAt
          comments {{
            totalCount
          }}
          commits {{
            totalCount
          }}
          createdAt
          deletions
          isDraft
          headRefOid
          headRefName
          labels (first: 10) {{
            nodes {{{label_info_query()}
            }}
          }}
          locked
          maintainerCanModify
          mergeCommit {{
            oid
          }}
          mergeable
          merged
          mergedAt
          mergedBy {{
            ... on User {{{user_info_query()}
            }}
          }}
          milestone {{{milestone_info_query()}
          }}
          id
          number
          state
          title
          updatedAt
          url
          author {{
            ... on User {{{user_info_query()}
            }}
          }}
        }}
        pageInfo {{
          hasNextPage
          endCursor
        }}
    }}
  }}
}}"""


def query_get_issues(cursor, owner, repository, limit):
    _cursor = "null" if cursor is None else ('"' + cursor + '"')
    return f"""
{{
  repository(owner: "{owner}", name: "{repository}") {{
    issues(first: {limit}, after: {_cursor}) {{
      totalCount
      nodes {{
        activeLockReason
        comments {{
          totalCount
        }}
        assignees (first: 10) {{
          nodes {{{user_info_query()}
          }}
        }}
        # pull_request: url
        milestone{{{milestone_info_query()}
        }}
        reactions (first: 100) {{
          nodes {{
            content
          }}
        }}
        body
        authorAssociation
        closedAt
        updatedAt
        createdAt
        state
        locked
        assignee: assignees (first: 1) {{
          nodes {{{user_info_query()}
          }}
        }}
        id
        number
        title
        labels (first: 10) {{
          nodes {{{label_info_query()}
          }}
        }}
        author {{
          ... on User{{{user_info_query()}
          }}
        }}
      }}
      pageInfo {{
        hasNextPage
        endCursor
      }}
    }}
  }}
}}
"""
