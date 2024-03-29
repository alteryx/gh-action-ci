from datetime import timedelta

from pytest import fixture, raises

from .. import github as gh

REPO = "alteryx/gh-action-ci"


@fixture()
def token(pytestconfig):
    return pytestconfig.getoption("github_token")


def test_latest_commit():
    commit = gh.latest_commit(repository=REPO)
    assert "author" in commit and "date" in commit["author"]


def test_latest_commit_branch():
    commit = gh.latest_commit(repository=REPO, branch="failed_workflow")
    assert "tree" in commit and "sha" in commit["tree"]
    assert commit["tree"]["sha"] == "cc5a32630a78f4ec3ef70f906c14a301aaf975cf"
    assert "d82a1c8151b01f51d7d9ceb39a0294feedbbc668" in commit["url"]


def test_not_recent_commit():
    commit = {"author": {"date": "1970-01-01"}}
    recent = gh.is_recent_commit(commit=commit, recent="days=7")
    assert not recent


def test_run_workflow(token):
    repo = "alteryx/featuretools-tsfresh-primitives"
    assert gh.run_workflow(repository=repo, workflow='tests.yml', token=token)


def test_recent_commit():
    commit = gh.latest_commit("alteryx/featuretools")
    recent = gh.is_recent_commit(commit=commit, recent="weeks=100000000")
    assert recent


def test_recent():
    actual = gh.api.check_recent("days=1, hours=1, seconds=1")
    expected = timedelta(days=1, hours=1, seconds=1)
    assert actual == expected


def test_invalid_recent():
    match = 'time value must be in a key-value pair format'
    with raises(ValueError, match=match):
        gh.api.check_recent("")


def test_default_branch():
    assert gh.default_branch(REPO) == 'main'


def test_workflow_success():
    assert gh.is_workflow_success(
        repository=REPO,
        workflow='Test GitHub CI',
        branch='test_workflow_success',
    )


def test_workflow_fail():
    assert not gh.is_workflow_success(
        repository=REPO,
        branch='test_workflow_fail',
        workflow='Test GitHub CI',
    )


def test_workflow_not_found():
    match = 'no workflow found for "unknown"'
    with raises(ValueError, match=match):
        gh.is_workflow_success(
            workflow='unknown',
            repository=REPO,
        )
