FROM python:3.7

ADD circleci circleci
ADD requirements.txt requirements.txt
ADD main.py main.py

RUN pip install pip --upgrade --progress-bar off
RUN pip install -r requirements.txt --progress-bar off
ENTRYPOINT ["python", "/main.py"]