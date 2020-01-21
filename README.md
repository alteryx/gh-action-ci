# GitHub Action - CircleCI

A GitHub Action for integrating CircleCI.

## Tasks

### `is_workflow_success`

|   Parameter  | Required | Description |
|:------------:|:--------:|:-----------:|
|  repository  |    yes   |             |
| circle-token |    yes   |             |

```yaml
- uses: featurelabs/gh-action-circleci@master
  with:
    task: is_workflow_success
    repository: ${{ github.repository }}
    circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

### `is_recent_commit`

|   Parameter  | Required | Description |
|:------------:|:--------:|:-----------:|
|  repository  |    yes   |             |
|    recent    |    yes   |             |

```yaml
- uses: featurelabs/gh-action-circleci@master
  with:
    task: is_recent_commit
    repository: featurelabs/featuretools
    recent: days=7
```

### `project_build`

|   Parameter  | Required | Description |
|:------------:|:--------:|:-----------:|
|  repository  |    yes   |             |
| circle-token |    yes   |             |

```yaml
- uses: featurelabs/gh-action-circleci@master
  with:
    task: project_build
    repository: ${{ github.repository }}
    circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

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

To install this workflow in your repository, add the lines above to `.github/workflows/circleci-scheduler.yml`. Then, add the following secret in the repository settings:

  - `CIRCLE_TOKEN`
