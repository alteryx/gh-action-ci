import os
import pytest
from . import latest_commit, latest_workflow, project_build

REPOSITORY = 'featurelabs/circleci-api'


@pytest.fixture()
def circle_token(pytestconfig):
    return pytestconfig.getoption("circle_token")


def test_latest_commit():
    commit = latest_commit('featurelabs/featuretools')
    keys_exist = ['author', 'message']
    keys_exist = [key in commit for key in keys_exist]
    assert all(keys_exist)


def test_latest_worklow(circle_token):
    workflow = latest_workflow(REPOSITORY, circle_token)
    assert not workflow.empty


def test_project_build(circle_token):
    response = project_build(REPOSITORY, circle_token)
    assert response['body'] == 'Build created'
