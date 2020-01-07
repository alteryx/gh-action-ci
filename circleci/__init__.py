import pandas as pd
import requests

CIRCLE_API = "https://circleci.com/api/v1.1"


def latest_commit(repository):
    url = "https://api.github.com/repos/%s/commits" % repository
    response = requests.get(url)
    assert response.status_code == 200, response
    json = response.json()
    commit = json[0]['commit']
    return commit


def latest_workflow(repository, circle_token=''):
    url = CIRCLE_API + "/project/github/{0}/tree/master?circle-token={1}"
    response = requests.get(url.format(repository, circle_token))

    assert response.status_code == 200, response
    integration_tests = response.json()
    assert integration_tests, 'no integration tests found'
    keys = ['workflow_id', 'workflow_name', 'job_name']

    records = []
    for test in integration_tests:
        record = test['workflows']
        values = map(record.get, keys)
        record = dict(zip(keys, values))
        record['status'] = test['status']
        records.append(record)

    df, key = pd.DataFrame(records), 'workflow_id'
    workflows, workflow_id = df.groupby(key, sort=False), df[key][0]
    workflow = workflows.get_group(workflow_id)
    return workflow


def project_build(repository, circle_token=''):
    url = CIRCLE_API + "/project/github/{0}/build?circle-token={1}"
    response = requests.post(url.format(repository, circle_token))
    assert response.status_code == 200, response
    return response.json()
