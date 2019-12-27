FROM python:3.7

ADD scripts scripts
ADD main.py main.py
RUN pip install pandas requests

ENTRYPOINT ["python", "/main.py"]