import pytest

from . import latest_commit, latest_workflow, project_build
from .utils import is_recent_commit, is_workflow_success

REPOSITORY = "featurelabs/gh-action-circleci"


@pytest.fixture()
def circle_token(pytestconfig):
    return pytestconfig.getoption("circle_token")


def test_latest_commit():
    commit = latest_commit("featurelabs/featuretools")
    assert "author" in commit and "date" in commit["author"]


def test_latest_commit_branch():
    commit = latest_commit("featurelabs/featuretools", branch="v0.1.10")
    assert "tree" in commit and "sha" in commit["tree"]
    assert commit["tree"]["sha"] == "ff46c8939833d022809d11694409eb1c0a18653f"
    assert "ace8d51435fe484476182e908c1ecf9515ec4918" in commit["url"]


def test_not_recent_commit():
    commit = {"author": {"date": "1970-01-01"}}
    recent = is_recent_commit(commit, recent="days=7")
    assert not recent


def test_project_build(circle_token):
    response = project_build(REPOSITORY, circle_token)
    assert response == "Build created"


def test_recent_commit():
    commit = latest_commit("featurelabs/featuretools")
    recent = is_recent_commit(commit, recent="weeks=100000000")
    assert recent


def test_workflow_failure(circle_token):
    workflow = latest_workflow(REPOSITORY, circle_token, status="failed",
                               branch='main')
    success = is_workflow_success(workflow)
    assert not success


def test_workflow_success(circle_token):
    workflow = latest_workflow(REPOSITORY, circle_token, status="successful",
                               branch='main')
    success = is_workflow_success(workflow)
    assert success
