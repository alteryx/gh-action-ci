# GitHub Action - CI

A GitHub Action integrated with the GitHub and CircleCI API.

#### Testing & Development

We are no longer testing the integration with CircleCI.

## Usage

This GitHub Action provides tasks that interface with the GitHub and CircleCI API. You can use these tasks to build workflows. In a workflow step, the task parameter must reference the task name, followed by any parameters.

```yaml
steps:
  - uses: alteryx/gh-action-ci@v3
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
| `branch` | The name of branch that contains the workflow. The default value is the default branch of the repository. | No |
| `workflow` | The name of the workflow to check for a successful status. | Yes |
| `token` | The token for making authorized requests to the CI provider's REST API. Only required for private repositories. | No |
| `ci` | The CI Provider for the task. The default value is `github` | No |

The returned value is a string data type that will either be `True` or `False`.

<hr>

### `run_workflow`

Create a dispatch event to run a workflow.

| Parameter | Description | Required |
|:---------:|-------------|:--------:|
| `repository` | The name of the repository that contains the workflow. | Yes |
| `workflow` | The file name of the workflow to dispatch. Only required for GitHub. | No |
| `token` | The token for making authorized requests to the CI provider's REST API. This can be a personal access token (PAT) with repo-scoped access for GitHub. | Yes |
| `ci` | The CI Provider for the task. The default value is `github` | No |

The returned value is a string data type. If the workflow was dispatched to run, the value will be `True`, otherwise `False`.

<br>

## Example - CircleCI Scheduler

This workflow uses the tasks to schedule project builds in CircleCI on recent commits to Featuretools.

```yaml
# circleci-scheduler.yml

on:
  schedule:
    # At 05:00 PM UTC
    - cron:  '0 17 * * *'

name: CircleCI Scheduler
jobs:
  Featuretools:
    runs-on: ubuntu-latest
    steps:
      - name: Check for successful workflow status in CircleCI.
        uses: alteryx/gh-action-ci@v3
        id: is_workflow_success
        with:
          task: is_workflow_success
          repository: ${{ github.repository }}
          token: ${{ secrets.CIRCLE_TOKEN }}
          ci: circleci

      - name: Check for recent commit to Featuretools.
        if: ${{ steps.is_workflow_success.outputs.value == 'True' }}
        uses: alteryx/gh-action-ci@v3
        id: is_recent_commit
        with:
          task: is_recent_commit
          repository: alteryx/featuretools
          recent: days=7

      - name: Trigger project build in CircleCI.
        if: ${{ steps.is_recent_commit.outputs.value == 'True' }}
        uses: alteryx/gh-action-ci@v3
        with:
          task: run_workflow
          repository: ${{ github.repository }}
          token: ${{ secrets.CIRCLE_TOKEN }}
          ci: circleci
```

To install this workflow, add the file above to the following location in your repository.

```
.github
└── workflows
    └── circleci-scheduler.yml
```

Then, add `CIRCLE_TOKEN` as a secret in your repository settings.
