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
    - name: Latest Status of Integration Tests
      uses: featurelabs/circleci-api@master

    - name: Check if a pull request was merged to Featuretools.
      uses: featurelabs/circleci-api@master
      # if: latest status of integration tests is successful

    - name: Run integration tests.
      uses: featurelabs/circleci-api@master
      # if: latest commit in Featuretools was within period
```

Then, add the following secrets to the repository settings:
  - `CIRCLE_TOKEN`

## Usage
