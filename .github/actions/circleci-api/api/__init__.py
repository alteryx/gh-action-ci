import pandas as pd
import requests


def latest_commit(repository):
    url = "https://api.github.com/repos/%s/commits" % repository
    response = requests.get(url)
    assert response.status_code == 200, response
    json = response.json()
    commit = json[0]['commit']
    return commit


def latest_workflow(repository, circle_token=''):
    url = "https://circleci.com/api/v1.1"
    url += "/project/github/{0}/tree/master"
    url += "?circle-token={1}&limit=5"
    response = requests.get(url.format(repository, circle_token))

    assert response.status_code == 200, response
    integration_tests = response.json()
    assert integration_tests, 'no integration tests found'

    records = []
    for test in integration_tests:
        if 'workflows' not in test: continue
        workflows = test['workflows']
        workflows['status'] = test['status']
        records.append(workflows)

    df, key = pd.DataFrame(records), 'workflow_id'
    assert not df.empty, 'no workflows found'
    workflows, workflow_id = df.groupby(key, sort=False), df[key][1]
    workflow = workflows.get_group(workflow_id)
    return workflow


def project_build(repository, circle_token=''):
    url = "https://circleci.com/api/v1.1"
    url += "/project/github/{0}/build?circle-token={1}"
    response = requests.post(url.format(repository, circle_token))
    assert response.status_code == 200, response
    return response.json()
