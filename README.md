# CircleCI Scheduler

A GitHub Action for scheduling CircleCI dynamically.

## Install

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
    - name: Checks the latest status on CircleCI.
      uses: featurelabs/circleci-api@master

    - name: Checks for recent commit to master on Featuretools.
      uses: featurelabs/circleci-api@master
      # if: latest status on CircleCI is successful

    - name: Triggers CircleCI
      uses: featurelabs/circleci-api@master
      # if: there was a recent commit to master on Featuretools
```

Then, add the following secrets to the repository settings:
  - `CIRCLE_TOKEN`

## Usage
