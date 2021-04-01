install:
	pip install -r requirements.txt --progress-bar off
	pip install -r test-requirements.txt --progress-bar off

lint-fix:
	autopep8  ci --in-place --recursive --max-line-length=100 \
	--select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	isort --recursive ci

lint-tests:
	flake8 ci --select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	isort --check-only --recursive ci

unit-tests:
	pytest ci/test/test_github.py --cov=ci/github --cache-clear --show-capture=stderr --disable-warnings -vv --github-token ${GITHUB_TOKEN}
