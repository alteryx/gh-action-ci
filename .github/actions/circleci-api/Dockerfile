FROM python:3.7
# ADD circleci /circleci
# ADD github /github
# ADD entrypoint.py /entrypoint.py
# ADD entrypoint.sh /entrypoint.sh

# WORKDIR /
COPY entrypoint.py entrypoint.py
RUN chmod +x entrypoint.py
ENTRYPOINT ["/entrypoint.py"]
