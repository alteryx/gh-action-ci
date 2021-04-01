from datetime import timedelta  # noqa
from datetime import datetime
from json import dumps

from dateutil.parser import parse
from requests import get, post

from ..utils import Color, check_status

REST_API = "https://api.github.com"


def default_branch(repository):
    url = f"{REST_API}/repos/{repository}"
    response = check_status(get(url), code=200)
    return response.json()['default_branch']


def check_recent(value):
    try:
        params = {}
        for param in value.split(','):
            param = param.lstrip().rstrip()
            key, value = param.split('=')
            params[key] = int(value)
        return timedelta(**params)
    except:
        raise ValueError('time value must be in a key-value pair format (i.e. weeks=1, days=1, hours=1, minutes=1)')


def is_recent_commit(commit, recent):
    recent = check_recent(recent)
    date = parse(commit['author']['date'])
    date = date.replace(tzinfo=None)
    elapsed = datetime.utcnow() - date
    recent = elapsed <= recent

    info = '\nThe latest commit {0} occurred {1} ago.\n'
    message = commit.get('message', '')
    message = message.splitlines()[:1]
    message = message.pop() if message else ''
    message = Color.YELLOW + message + Color.END

    relative = str(elapsed).split('.')[0]
    relative = relative.replace(',', '')
    color = Color.GREEN if recent else Color.RED
    relative = color + relative + Color.END
    print(info.format(message, relative))
    return recent


def latest_commit(repository, branch=None):
    url = f"{REST_API}/repos/{repository}/commits"
    branch = {"sha": branch or default_branch(repository)}
    response = check_status(get(url, params=branch), code=200)
    commit = response.json()[0]["commit"]
    return commit


def is_workflow_success(repository, branch=None, workflow=None, status='completed'):
    branch = branch or default_branch(repository)
    url = f"{REST_API}/repos/{repository}/actions/runs?per_page=100"
    response = check_status(get(url), code=200).json()

    for run in response['workflow_runs']:
        not_branch = branch != run['head_branch']
        not_name = workflow and workflow != run['name']
        not_status = status != run['status']
        print(run['head_branch'], run['name'], run['status'])
        if not_branch or not_name or not_status: continue
        return run['conclusion'] == 'success'

    info = 'no workflow found'
    if workflow: info += f' for "{workflow}"'
    raise ValueError(info)


def run_workflow(repository, workflow, token, branch='main'):
    url = f"{REST_API}/repos/{repository}/actions/workflows/{workflow}/dispatches"
    headers = {'Accept': 'application/vnd.github.v3+json', 'Authorization': f'token {token}'}
    branch = dumps({"ref": branch or default_branch(repository)})
    check_status(post(url, headers=headers, data=branch), code=204)
    return True
