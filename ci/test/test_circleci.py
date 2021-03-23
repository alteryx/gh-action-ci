from pytest import fixture, mark

from ci import circleci

REPO = 'FeatureLabs/gh-action-circleci'


@fixture()
def token(pytestconfig):
    return pytestconfig.getoption('circle_token')


@mark.parametrize('branch', [(None), ('main'), ('v1')])
def test_run_workflow(token, branch):
    assert circleci.run_workflow(REPO, token, branch=branch)


@mark.parametrize('branch', [(None), ('main'), ('failed_workflow')])
def test_workflow_failure(token, branch):
    success = circleci.is_workflow_success(
        REPO,
        token,
        status='failed',
        branch=branch,
    )
    assert not success


@mark.parametrize('branch', [(None), ('main'), ('v1')])
def test_workflow_success(token, branch):
    success = circleci.is_workflow_success(
        REPO,
        token,
        status='successful',
        branch=branch,
    )
    assert success
