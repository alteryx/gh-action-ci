from urllib.parse import quote_plus

import pandas as pd
from requests import get, post

from ..github import default_branch
from ..utils import check_status

REST_API = "https://circleci.com/api/v1.1"


def is_workflow_success(repository, branch='main', workflow=None, status='completed', token=''):
    # CircleCI API requires url-encoded branch
    branch = quote_plus(branch or default_branch(repository))
    url = f"{REST_API}/project/github/{repository}/tree"
    url += f"/{branch}?circle-token={token}&filter={status}"
    tests = check_status(get(url), code=200).json()
    if not tests: return

    df = pd.DataFrame({
        'workflow_id': test['workflows']['workflow_id'],
        'workflow_name': test['workflows']['workflow_name'],
        'job_name': test['workflows']['job_name'],
        'status': test['status'],
    } for test in tests)

    if workflow is not None:
        df = df[df.workflow_name.eq(workflow)]
        if df.empty: return

    workflows = df.groupby("workflow_id", sort=False)
    latest_workflow = df["workflow_id"][0]
    group = workflows.get_group(latest_workflow)
    success = group.status.eq('success').all()
    return success


def run_workflow(repository, token, branch=None):
    # CircleCI API requires url-encoded branch
    branch = {"branch": quote_plus(branch or default_branch(repository))}
    url = f"{REST_API}/project/github/{repository}/build?circle-token={token}"
    response = check_status(post(url, data=branch), code=200).json()
    assert response['body'] == 'Build created', response['body']
    return True
