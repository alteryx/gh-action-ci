FROM python:3.7

# ADD circleci /circleci
# ADD github /github
# ADD entrypoint.py /entrypoint.py
# ADD entrypoint.sh /entrypoint.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
