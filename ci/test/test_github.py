from pytest import fixture

from ci import github as gh

REPO = "featurelabs/gh-action"


@fixture()
def token(pytestconfig):
    return pytestconfig.getoption("github_token")


def test_latest_commit():
    commit = gh.latest_commit(REPO)
    assert "author" in commit and "date" in commit["author"]


def test_latest_commit_branch():
    commit = gh.latest_commit("featurelabs/featuretools", branch="v0.1.10")
    assert "tree" in commit and "sha" in commit["tree"]
    assert commit["tree"]["sha"] == "ff46c8939833d022809d11694409eb1c0a18653f"
    assert "ace8d51435fe484476182e908c1ecf9515ec4918" in commit["url"]


def test_not_recent_commit():
    commit = {"author": {"date": "1970-01-01"}}
    recent = gh.is_recent_commit(commit, recent="days=7")
    assert not recent


def test_workflow_dispatch(token):
    repo = "featurelabs/featuretools-tsfresh-primitives"
    assert gh.run_workflow(repo, 'tests.yml', token)


def test_recent_commit():
    commit = gh.latest_commit("featurelabs/featuretools")
    recent = gh.is_recent_commit(commit, recent="weeks=100000000")
    assert recent


def test_default_branch():
    assert gh.default_branch(REPO) == 'main'
