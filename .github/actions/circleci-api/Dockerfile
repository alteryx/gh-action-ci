FROM python:3.7

ADD api.py api.py
ADD main.py main.py
RUN pip install pandas requests -q

ENTRYPOINT ["python", "/main.py"]