from pytest import fixture

from ci import github as gh

REPO = "FeatureLabs/gh-action-circleci"


@fixture()
def token(pytestconfig):
    return pytestconfig.getoption("github_token")


def test_latest_commit():
    commit = gh.latest_commit(REPO)
    assert "author" in commit and "date" in commit["author"]


def test_latest_commit_branch():
    commit = gh.latest_commit(REPO, branch="failed_workflow")
    assert "tree" in commit and "sha" in commit["tree"]
    assert commit["tree"]["sha"] == "cc5a32630a78f4ec3ef70f906c14a301aaf975cf"
    assert "d82a1c8151b01f51d7d9ceb39a0294feedbbc668" in commit["url"]


def test_not_recent_commit():
    commit = {"author": {"date": "1970-01-01"}}
    recent = gh.is_recent_commit(commit, recent="days=7")
    assert not recent


def test_run_workflow(token):
    repo = "alteryx/featuretools-tsfresh-primitives"
    assert gh.run_workflow(repo, 'tests.yml', token)


def test_recent_commit():
    commit = gh.latest_commit("alteryx/featuretools")
    recent = gh.is_recent_commit(commit, recent="weeks=100000000")
    assert recent


def test_default_branch():
    assert gh.default_branch(REPO) == 'main'


def test_workflow_success(token):
    assert gh.is_workflow_success(REPO, name='Test Suite')
