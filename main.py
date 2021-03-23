from ci import circleci, github
from argparse import ArgumentParser


def main():
    task = ArgumentParser()
    task.add_argument('name')
    task.add_argument('repository')
    task.add_argument('--recent', default='days=30')
    task.add_argument('--token')
    task.add_argument('--branch', default=None)
    task = task.parse_args()

    if task.name == 'is_workflow_success':
        if task.ci.lower() == 'circleci':
            value = circleci.is_workflow_success(
                repository=task.repository,
                token=task.token,
                branch=task.branch,
            )
            print(f"::set-output name=value::{value}")

        elif task.ci.lower() == 'github':
            value = github.is_workflow_success(
                repository=task.repository,
                name=task.workflow,
                branch=task.branch,
            )
            print(f"::set-output name=value::{value}")

    elif task.name == 'is_recent_commit':
        commit = github.latest_commit(task.repository, task.branch)
        recent = github.is_recent_commit(commit, recent=task.recent)
        print(f"::set-output name=value::{recent}")

    elif task.name == 'run_workflow':
        if task.ci.lower() == 'circleci':
            value = circleci.run_workflow(
                repository=task.repository,
                token=task.token,
                branch=task.branch,
            )
            print(f"::set-output name=value::{value}")

        elif task.ci.lower() == 'github':
            value = github.run_workflow(
                repository=task.repository,
                workflow=task.workflow,
                token=task.token,
                branch=task.branch,
            )
            print(f"::set-output name=value::{value}")

    else:
        raise ValueError('task not supported')


if __name__ == '__main__':
    main()
