FROM python:3.7

# Package Installation
ADD circleci circleci
ADD requirements.txt requirements.txt
ADD setup.py setup.py
RUN pip install .

# Entry Point
ADD main.sh main.sh
ENTRYPOINT [ "main.sh" ]
