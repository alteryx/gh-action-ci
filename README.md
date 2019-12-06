# CircleCI Scheduler

A GitHub Action for scheduling CircleCI dynamically.

## Install

In your repository, add the following lines to `.github/workflows/release.yml`:

```yaml
on:
  schedule:
    - cron:  '*/5 * * * *'

name: CircleCI Scheduler
jobs:
  Featuretools:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@master
    - uses: FeatureLabs/circleci-scheduler@master
      env:
        REPOSITORY: featurelabs/featuretools
        EVENT: Latest Commit to Master
        CRON: '*/5 * * * *'
        TOKEN : <TOKEN>
```

Then, add the following secrets to the repository settings:
  - `TOKEN`

## Usage
