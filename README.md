# GitHub Action - CircleCI

A GitHub Action for integrating CircleCI.

## Tasks

This should be an explanation for what the tasks are and how to use them.

### `is_workflow_success`

This task will check whether the latest workflow completed successfully in CircleCI. 

|  Parameters  | Required |                  Description                     |
|:------------:|:--------:|:------------------------------------------------:|
|  repository  |    yes   |    The repository to check for a sucessful workflow status.   |
| circle-token |    yes   | A personal API token to access the CircleCI API. |

The returned value is a string data type that will either be `True` or `False`. The value can be accessed in successive workflow steps by using the `value` output.

```
steps.<step id>.outputs.value
```

This should be an explanation for the following code snippet.

```yaml
- name: Check for successful workflow status in CircleCI.
  uses: featurelabs/gh-action-circleci@master
  id: is_workflow_success
  with:
    task: is_workflow_success
    repository: ${{ github.repository }}
    circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

<hr>

### `is_recent_commit`

This task will check whether the latest commit happened recently in GitHub. The latest commit will be used from the default branch of a public repository.

|  Parameters  | Required | Description |
|:------------:|:--------:|:-----------:|
|  repository  |    yes   | The public repository to check for a recent commit. |
|    recent    |    yes   | The period used to define whether a commit happened recently. |

The returned value is a string data type that will either be `True` or `False`. The value can be accessed in successive workflow steps by using the `value` output.

```
steps.<step id>.outputs.value
```

This should be an explanation for the following code snippet.

```yaml
- uses: featurelabs/gh-action-circleci@master
  with:
    task: is_recent_commit
    repository: featurelabs/featuretools
    recent: days=7
```

### `project_build`

This task will trigger a project build in CircleCI.

|  Parameters  | Required | Description |
|:------------:|:--------:|:-----------:|
|  repository  |    yes   | The repository to build. |
| circle-token |    yes   | A personal API token to access the CircleCI API. |

The returned value is a string data type. The value is the response message from CircleCI and can be accessed in successive workflow steps by using the `value` output.

```
steps.<step id>.outputs.value
```

This should be an explanation for the following code snippet.

```yaml
- uses: featurelabs/gh-action-circleci@master
  with:
    task: project_build
    repository: ${{ github.repository }}
    circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

<br>

## Example

This workflow uses the tasks to schedule project builds in CircleCI on recent commits to Featuretools.

```yaml
on:
  schedule:
    # At 12:00 on every day-of-week from Monday through Friday.
    - cron:  '0 12 * * 1-5'

name: CircleCI Scheduler
jobs:
  featuretools:
    runs-on: ubuntu-latest
    steps:
      - name: Check for successful workflow status in CircleCI.
        uses: featurelabs/gh-action-circleci@master
        id: is_workflow_success
        with:
          task: is_workflow_success
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}

      - if: contains(steps.is_workflow_success.outputs.value, 'True')
        name: Check for recent commit to Featuretools.
        uses: featurelabs/gh-action-circleci@master
        id: is_recent_commit
        with:
          task: is_recent_commit
          repository: featurelabs/featuretools
          recent: days=7

      - if: contains(steps.is_recent_commit.outputs.value, 'True')
        name: Trigger project build in CircleCI.
        uses: featurelabs/gh-action-circleci@master
        with:
          task: project_build
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

To install this workflow, add the lines above to `.github/workflows/circleci-scheduler.yml`. Then, add `CIRCLE_TOKEN` as a secret in your repository settings.
