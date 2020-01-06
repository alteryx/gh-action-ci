FROM python:3.7

ADD circleci circleci
ADD main.py main.py
RUN pip install pandas requests --progress-bar off
RUN pip install pip --upgrade --progress-bar off

ENTRYPOINT ["python", "/main.py"]