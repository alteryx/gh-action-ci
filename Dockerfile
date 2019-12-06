FROM python:3.7

LABEL "com.github.actions.name"="CircleCI Scheduler"
LABEL "com.github.actions.description"="A GitHub Action for scheduling CircleCI dynamically."

LABEL "repository"="circleci-scheduler"
LABEL "maintainer"="support@featurelabs.com"

ADD upload.sh /upload.sh
RUN ["chmod", "+x", "main.sh"]
ENTRYPOINT ["/main.sh"]
