def userInfoQuery():
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


def labelInfoQuery():
    return """
        color
        description
        name
        url"""


def milestoneInfoQuery():
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


def queryGetPullRequests(cursor, owner, repository, limit):
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
            nodes {{{userInfoQuery()}
            }}
          }}
          assignees (first: 10) {{
            nodes {{{userInfoQuery()}
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
            nodes {{{labelInfoQuery()}
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
            ... on User {{{userInfoQuery()}
            }}
          }}
          milestone {{{milestoneInfoQuery()}
          }}
          id
          number
          state
          title
          updatedAt
          url
          author {{
            ... on User {{{userInfoQuery()}
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


def queryGetIssues(cursor, owner, repository, limit):
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
          nodes {{{userInfoQuery()}
          }}
        }}
        # pull_request: url
        milestone{{{milestoneInfoQuery()}
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
          nodes {{{userInfoQuery()}
          }}
        }}
        id
        number
        title
        labels (first: 10) {{
          nodes {{{labelInfoQuery()}
          }}
        }}
        author {{
          ... on User{{{userInfoQuery()}
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
