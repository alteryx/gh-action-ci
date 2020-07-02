# GitHub Action - CircleCI

A GitHub Action for integrating CircleCI.

## Usage

This GitHub Action provides tasks that interface with CircleCI. These tasks can be used to build workflows. In a workflow step, the `task` parameter must reference the name of a task. This is followed by any parameters for the task.

```yaml
steps:
  - uses: featurelabs/gh-action-circleci@v2
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

### `is_workflow_success`

This will check whether the latest workflow completed successfully in CircleCI.

| Parameters   | Required | Description                                                                            |
|--------------|----------|----------------------------------------------------------------------------------------|
| repository   | yes      | The repository to check for a sucessful workflow status.                               |
| circle-token | yes      | A personal API token to access the CircleCI API.                                       |
| branch       | no       | The branch to check against. If none is specified, uses default branch for repository. |

The returned value is a string data type that will either be `True` or `False`.

<hr>

### `is_recent_commit`

This will check whether the latest commit happened recently in GitHub. The latest commit will be used from the default branch of a public repository.

| Parameters | Required | Description                                                                                                                                                        |
|------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| repository | yes      | The public repository to check for a recent commit.                                                                                                                |
| recent     | yes      | The period used to define whether a commit happened recently. The time value must be in a key-value pair format (i.e. `weeks=1, days=1, hours=1, minutes=1`, etc.) |
| branch     | no       | The branch to check against. If none is specified, uses default branch for repository.                                                                             |

The returned value is a string data type that will either be `True` or `False`.

<hr>

### `project_build`

This will trigger a project build in CircleCI.

| Parameters   | Required | Description                                                                                          |
|--------------|----------|------------------------------------------------------------------------------------------------------|
| repository   | yes      | The repository to build.                                                                             |
| circle-token | yes      | A personal API token to access the CircleCI API.                                                     |
| branch       | no       | The branch to check against. If none is specified, uses default branch for repository.               |

The returned value is a string data type. If the project build was triggered, the value will be `True`, otherwise `False`.

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
