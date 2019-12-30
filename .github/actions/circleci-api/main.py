import api
from argparse import ArgumentParser
from dateutil.parser import parse
from datetime import datetime, timedelta

class colors:
    END = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'

def is_recent_commit(commit, recent):
    recent = eval('timedelta(%s)' % recent)
    date = parse(commit['author']['date'])
    date = date.replace(tzinfo=None)
    elapsed = datetime.utcnow() - date
    recent = elapsed <= recent

    # Print status of the latest commit.
    info = 'The latest commit {0} occurred {1} ago.'
    message = commit['message'].splitlines()[0]    
    message = colors.YELLOW + message + colors.END
    relative = str(elapsed).split('.')[0]
    relative = relative.replace(',', '')
    color = colors.GREEN if recent else colors.RED
    relative = color + relative + colors.END
    print(info.format(message, relative))

    return recent


def main():
    task = ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--recent', default='days=30')
    task.add_argument('--circle-token')
    task = task.parse_args()

    if task.name == 'latest_workflow_status':
        workflow = api.latest_workflow(task.repository, task.circle_token)

        line = '-' * 25
        print('\n', line, ' Latest Status on CircleCI ', line, '\n')
        keys = ['workflow_id', 'workflow_name', 'job_name', 'status']
        print(workflow[keys].to_string(index=False), '\n')

        success = workflow.status.eq('success').all()
        assert success, 'latest workflow was not successful'

    elif task.name == 'is_recent_commit':
        commit = api.latest_commit(task.repository)
        recent = is_recent_commit(commit, recent=task.recent)
        assert recent, 'latest commit was not recent'

    elif task.name == 'project_build':
        reponse = api.project_build(task.repository, task.circle_token)
        print(reponse['body'])

    else:
        raise ValueError('task not supported')


if __name__ == '__main__':
    main()
