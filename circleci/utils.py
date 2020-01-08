from datetime import datetime, timedelta  # noqa

from dateutil.parser import parse


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
    info = '\nThe latest commit {0} occurred {1} ago.\n'
    message = commit.get('message', '')
    message = message.splitlines()[:1]
    message = message.pop() if message else ''
    message = colors.YELLOW + message + colors.END

    relative = str(elapsed).split('.')[0]
    relative = relative.replace(',', '')
    color = colors.GREEN if recent else colors.RED
    relative = color + relative + colors.END
    print(info.format(message, relative))
    return recent


def is_workflow_success(workflow):
    print('\n', workflow.to_string(index=False), '\n')
    success = workflow.status.eq('success').all()
    return success
