from pytest import fixture, mark

from .. import circleci

REPO = 'FeatureLabs/gh-action-ci'


@fixture()
def token(pytestconfig):
    return pytestconfig.getoption('circle_token')


@mark.parametrize('branch', [(None), ('main'), ('v1')])
def test_run_workflow(token, branch):
    assert circleci.run_workflow(
        repository=REPO,
        branch=branch,
        token=token,
    )


@mark.parametrize('branch', [(None), ('main'), ('failed_workflow')])
def test_workflow_failure(token, branch):
    success = circleci.is_workflow_success(
        repository=REPO,
        status='failed',
        branch=branch,
        token=token,
    )
    assert not success


@mark.parametrize('branch', [(None), ('main'), ('v1')])
def test_workflow_success(token, branch):
    success = circleci.is_workflow_success(
        repository=REPO,
        workflow='workflow',
        status='successful',
        branch=branch,
        token=token,
    )
    assert success
