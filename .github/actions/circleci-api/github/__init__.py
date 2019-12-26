import requests


class api:
    def __init__(self, username, project):
        self.username = username
        self.project = project
    
    def get_commits(self, since=None):
        parameters = {'username': self.username, 'project': self.project}
        url = "https://api.github.com/repos/{username}/{project}/commits"
        if since: url += "?since=%s" % since        
        url = url.format(**parameters)
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()