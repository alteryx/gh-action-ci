import os
import pytest
from . import latest_commit, latest_workflow, project_build, utils

REPOSITORY = 'featurelabs/circleci-api'


@pytest.fixture()
def circle_token(pytestconfig):
    return pytestconfig.getoption("circle_token")


@pytest.fixture()
def commit():
    return {'author': {'date': '1970-01-01'}}


def test_latest_commit():
    commit = latest_commit('featurelabs/featuretools')
    assert 'author' in commit and 'date' in commit['author']


def test_project_build(circle_token):
    response = project_build(REPOSITORY, circle_token)
    assert response['body'] == 'Build created'


def test_recent_commit(commit):
    recent = utils.is_recent_commit(commit, recent='days=7')
    assert not recent


def test_workflow_success(circle_token):
    workflow = latest_workflow(REPOSITORY, circle_token)
    success = utils.is_workflow_success(workflow)
    assert success
