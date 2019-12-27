import pandas as pd
import requests


def latest_commit(repository):
    url = "https://api.github.com/repos/{repository}/commits" % repository
    # if since: url += "?since=%s" % since
    response = requests.get(url)
    assert response.status_code == 200, response
    json = response.json()
    return json



def latest_workflow(repository, circle_token=''):
    url = "https://circleci.com/api/v1.1"
    url += "/project/github/{repository}/tree/master"
    url += "?circle-token={token}&limit=5&offset=5&filter=completed"
    url = url.format(repository=repository, token=circle_token)
    response = requests.get(url)

    assert response.status_code == 200, response
    json = response.json()
    records = []

    for test in json:
        workflows = test['workflows']
        workflows['status'] = test['status']
        records.append(workflows)

    df, key = pd.DataFrame(records), 'workflow_id'
    workflows, workflow_id = df.groupby(key, sort=False), df[key][1]
    workflow = workflows.get_group(workflow_id)
    return workflow


def project_build(repository, circle_token=''):
    pass
