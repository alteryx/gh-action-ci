from ci import circleci, github
from argparse import ArgumentParser


def main():
    task = ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--recent', default='days=30')
    task.add_argument('--token')
    task.add_argument('--branch', default=None)
    task.add_argument('--ci', default='github')
    task = task.parse_args()

    ci = task.ci.lower()
    if task.name == 'is_workflow_success':
        if ci == 'circleci':
            value = circleci.is_workflow_success(
                repository=task.repository,
                branch=task.branch,
                token=task.token,
            )
            print(f"::set-output name=value::{value}")

        elif ci == 'github':
            value = github.is_workflow_success(
                repository=task.repository,
                workflow=task.workflow,
                branch=task.branch,
            )
            print(f"::set-output name=value::{value}")

    elif task.name == 'is_recent_commit':
        commit = github.latest_commit(task.repository, task.branch)
        recent = github.is_recent_commit(commit, recent=task.recent)
        print(f"::set-output name=value::{recent}")

    elif task.name == 'run_workflow':
        if ci == 'circleci':
            value = circleci.run_workflow(
                repository=task.repository,
                branch=task.branch,
                token=task.token,
            )
            print(f"::set-output name=value::{value}")

        elif ci == 'github':
            value = github.run_workflow(
                repository=task.repository,
                workflow=task.workflow,
                branch=task.branch,
                token=task.token,
            )
            print(f"::set-output name=value::{value}")

    else:
        raise ValueError('task not supported')


if __name__ == '__main__':
    main()
