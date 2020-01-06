# CircleCI API

A GitHub Action for integrating CircleCI.

## Examples

### CircleCI Scheduler

This workflow uses the GitHub Action to schedule CircleCI on recent commits to Featuretools.

#### Install

In your repository, add the following lines to `.github/workflows/circleci-scheduler.yml`:

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
        uses: featurelabs/circleci-api@master
        id: is_workflow_success
        with:
          task: is_workflow_success
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}

      - if: contains(steps.is_workflow_success.outputs.value, 'True')
        name: Check for recent commit to Featuretools.
        uses: featurelabs/circleci-api@master
        id: is_recent_commit
        with:
          task: is_recent_commit
          repository: featurelabs/featuretools
          recent: days=7

      - if: contains(steps.is_recent_commit.outputs.value, 'True')
        name: Trigger project build in CircleCI.
        uses: featurelabs/circleci-api@master
        with:
          task: project_build
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

Then, add the following secrets to the repository settings:

  - `CIRCLE_TOKEN`
