# CircleCI API

A GitHub Action for integrating with CircleCI.

## Examples

### CircleCI Scheduler

This workflow uses the GitHub Action to schedule CircleCI on recent commits to Featuretools.

#### Install

In your repository, add the following lines to `.github/workflows/circleci-scheduler.yml`:

```yaml
on:
  schedule:
    - cron:  '*/5 * * * *'

name: CircleCI Scheduler
jobs:
  featuretools:
    runs-on: ubuntu-latest
    steps:
      - name: Check for successful workflow status on CircleCI.
        uses: featurelabs/circleci-api@master
        with:
          task: is_workflow_success
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}

      - if: success()
        name: Check for recent commit to Featuretools.
        uses: featurelabs/circleci-api@master
        with:
          task: is_recent_commit
          repository: featurelabs/featuretools
          recent: days=7

      - if: success()
        name: Trigger project build on CircleCI.
        uses: featurelabs/circleci-api@master
        with:
          task: project_build
          repository: ${{ github.repository }}
          circle-token: ${{ secrets.CIRCLE_TOKEN }}
```

Then, add the following secrets to the repository settings:

  - `CIRCLE_TOKEN`
