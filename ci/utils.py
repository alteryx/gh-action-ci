class Color:
    END = '\033[0m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'


def check_status(response, code=200):
    info = "%s (%s)" % (response.reason, response.status_code)
    assert response.status_code == code, info
    return response
