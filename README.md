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
  Featuretools:
    runs-on: ubuntu-latest
    steps:
    - name: Check latest build status in local project.
      uses: featurelabs/circleci-api@master

    - name: Check latest build time in Featuretools.
      uses: featurelabs/circleci-api@master
      # if: latest build status in local project was successful

    - name: Trigger build in local project.
      uses: featurelabs/circleci-api@master
      # if: latest build time in Featuretools was within the past period
```

Then, add the following secrets to the repository settings:
  - `CIRCLE_TOKEN`

## Usage