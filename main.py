import circleci
from argparse import ArgumentParser


def main():
    task = ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--recent', default='days=30')
    task.add_argument('--circle-token')
    task.add_argument('--branch', default=None)
    task = task.parse_args()

    if task.name == 'is_workflow_success':
        workflow = circleci.latest_workflow(task.repository, task.circle_token,
                                            task.branch)
        success = circleci.is_workflow_success(workflow)
        print("::set-output name=value::%s" % success)

    elif task.name == 'is_recent_commit':
        commit = circleci.latest_commit(task.repository, task.branch)
        recent = circleci.is_recent_commit(commit, recent=task.recent)
        print("::set-output name=value::%s" % recent)

    elif task.name == 'project_build':
        response = circleci.project_build(task.repository, task.circle_token,
                                          task.branch)
        print("::set-output name=value::%s" % response == 'Build created')
        print(response)

    else:
        raise ValueError('task not supported')


if __name__ == '__main__':
    main()
