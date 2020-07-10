from pydantic import BaseModel


class RepositoryLinkIds(BaseModel):
    owner: str
    repository: str
    algorithm: str


class Repository(BaseModel):
    owner: str
    repository: str


class RepositoryLimited(BaseModel):
    owner: str
    repository: str
    limit = 0


class RepositoryLimitedIssues(BaseModel):
    owner: str
    repository: str
    limit = 0
    pr_as_issue = False


class RepositoryMetrics(BaseModel):
    ci: int
    license: int
    history: float
    management: float
    documentation: float
    community: int
    tests: float
