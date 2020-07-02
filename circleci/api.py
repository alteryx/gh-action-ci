import pandas as pd
import requests

CIRCLE_API = "https://circleci.com/api/v1.1"


def latest_commit(repository, branch=None):
    params = {}
    if branch is not None:
        params["sha"] = branch
    url = "https://api.github.com/repos/%s/commits" % repository
    print(params)
    response = requests.get(url, params=params)
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == 200, info
    json = response.json()
    commit = json[0]["commit"]
    return commit


def latest_workflow(repository, circle_token="", status="completed",
                    branch="main"):
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
    url = CIRCLE_API + "/project/github/{0}/build?circle-token={1}"
    if branch is not None:
        url += "?branch={}".format(branch)
    response = requests.post(url.format(repository, circle_token))
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == 200, info
    return response.json()["body"]
