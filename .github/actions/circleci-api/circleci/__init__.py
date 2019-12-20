import requests

class api:
    def __init__(self, vcs_type, username, project, token):
        self.vcs_type = vcs_type
        self.username = username
        self.project = project
        self.token = token
    
    def recent_builds(self, limit=20, offset=5, filter='completed'):
        parameters = dict(
            vcs_type=self.vcs_type,
            username=self.username,
            project=self.project,
            limit=limit,
            offset=offset,
            filter=filter,
        )

        url = "https://circleci.com/api/v1.1/project/{vcs_type}/{username}/{project}?limit={limit}&offset={offset}&filter={filter}"
        url = url.format(**parameters)
        response = requests.get(url)
        return response.json()
