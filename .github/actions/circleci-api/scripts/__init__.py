import pandas as pd
import requests

def latest_workflow_status(repository, token=''):
    url = "https://circleci.com/api/v1.1"
    url += "/project/github/{repository}/tree/master"
    url += "?circle-token={token}&limit=5&offset=5&filter=completed"
    url = url.format(repository=repository, token=token)
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
    latest_workflow = workflows.get_group(workflow_id)

    keys = ['workflow_id', 'workflow_name', 'job_name', 'status']
    string = '\n' + latest_workflow[keys].to_string(index=False) + '\n'
    print(string)

    return latest_workflow.status.eq('success').all()
