FROM python:3.7
# ADD circleci /circleci
# ADD github /github
# ADD entrypoint.py /entrypoint.py
# ADD entrypoint.sh /entrypoint.sh

WORKDIR /app
RUN pwd
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh
RUN pwd
ENTRYPOINT /app/entrypoint.sh
