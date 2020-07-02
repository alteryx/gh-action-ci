import urllib.parse

import pandas as pd
import requests

CIRCLE_API = "https://circleci.com/api/v1.1"


def latest_commit(repository, branch=None):
    if branch is None:
        branch = default_branch(repository)
    url = f"https://api.github.com/repos/{repository}/commits"
    response = requests.get(url, params={"sha": branch})
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == 200, info
    json = response.json()
    commit = json[0]["commit"]
    return commit


def latest_workflow(repository, circle_token="", status="completed",
                    branch=None):
    if branch is None:
        branch = default_branch(repository)
    # CircleCI API requires url-encoded branch
    branch = urllib.parse.quote_plus(branch)
    url = CIRCLE_API + f"/project/github/{repository}/tree"
    url += f"/{branch}?circle-token={circle_token}&filter={status}"
    response = requests.get(url)
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == 200, info
    integration_tests = response.json()
    assert integration_tests, "no integration tests found"
    keys = ["workflow_id", "workflow_name", "job_name"]

    records = []
    for test in integration_tests:
        record = test["workflows"]
        record = {key: record[key] for key in keys}
        record["status"] = test["status"]
        records.append(record)
    df, key = pd.DataFrame(records), "workflow_id"
    workflows, workflow_id = df.groupby(key, sort=False), df[key][0]
    workflow = workflows.get_group(workflow_id)
    return workflow


def project_build(repository, circle_token="", branch=None):
    if branch is None:
        branch = default_branch(repository)
    # CircleCI API requires url-encoded branch
    branch = urllib.parse.quote_plus(branch)
    url = CIRCLE_API
    url += f"/project/github/{repository}/build?circle-token={circle_token}"
    response = requests.post(url, data={"branch": branch})
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == 200, info
    return response.json()["body"]


def default_branch(repository):
    url = f"https://api.github.com/repos/{repository}"
    response = requests.get(url)
    info = f"{repository} not found"
    assert response.status_code == 200, info
    data = response.json()
    return data['default_branch']
