# GitHub Action - CI

A GitHub Action integrated with the GitHub REST API and CircleCI.

## Usage

This GitHub Action provides tasks that interface with the GitHub REST API. You can use these tasks to build workflows. In a workflow step, the task parameter must reference the task name, followed by any parameters.

```yaml
steps:
  - uses: featurelabs/gh-action-github@v1
    id: <step id>
    with:
      task: <task name>
      # ... parameters for the task
```

The returned value of a task is available in later steps from the output `value`.

```
steps.<step id>.outputs.value
```

## Tasks

This is a list of the available tasks:

### `is_recent_commit`

Check whether the latest commit happened recently.

| Parameter | Description | Required |
|:---------:|-------------|:--------:|
| `repository` | The name of the public repository that contains the commit. | Yes |
| `branch` | The name of branch that contains the commit. The default value is the default branch of the repository. | No |
| `recent` | The period used to define whether a commit happened recently. The time value must be in a key-value pair format (i.e. `weeks=1, days=1, hours=1, minutes=1`, etc.) The default value is seven days. | No |

The returned value is a string data type that will either be `True` or `False`.

<hr>

### `is_workflow_success`

Check whether the latest workflow completed successfully.

| Parameter | Description | Required |
|:---------:|-------------|:--------:|
| `repository` | The name of the public repository that contains the workflow. | Yes |
| `workflow` | The name of the workflow to check for a successful status. | Yes |

The returned value is a string data type that will either be `True` or `False`.

<hr>

### `run_workflow`

Create a dispatch event to run a workflow.

| Parameter | Description | Required |
|:---------:|-------------|:--------:|
| `repository` | The name of the repository that contains the workflow. | Yes |
| `workflow` | The file name of the workflow to dispatch. | Yes |
| `token` | The personal access token (PAT) with repo-scoped access. | Yes |

The returned value is a string data type. If the workflow was dispatched to run, the value will be `True`, otherwise `False`.

<br>

## Example - CircleCI Scheduler Workflow

This workflow uses the tasks to schedule project builds in CircleCI on recent commits to Featuretools.

```yaml
# circleci-scheduler.yml

on:
  schedule:
    # At 12:00 on every day-of-week from Monday through Friday.
    - cron:  '0 12 * * 1-5'

name: CircleCI Scheduler
jobs:
  Featuretools:
    runs-on: ubuntu-latest
    steps:
      - name: Check for successful workflow status in CircleCI.
        uses: featurelabs/gh-action-circleci@v2
        id: is_workflow_success
        with:
          task: is_workflow_success
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}
          branch: main

      - if: contains(steps.is_workflow_success.outputs.value, 'True')
        name: Check for recent commit to Featuretools.
        uses: featurelabs/gh-action-circleci@v2
        id: is_recent_commit
        with:
          task: is_recent_commit
          repository: featurelabs/featuretools
          recent: days=7

      - if: contains(steps.is_recent_commit.outputs.value, 'True')
        name: Trigger project build in CircleCI.
        uses: featurelabs/gh-action-circleci@v2
        with:
          task: project_build
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

To install this workflow, add the file above to the following location in your repository.

```
.github
└── workflows
    └── circleci-scheduler.yml
```

Then, add `CIRCLE_TOKEN` as a secret in your repository settings.
