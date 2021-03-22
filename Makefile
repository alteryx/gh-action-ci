install:
	pip install -r requirements.txt --progress-bar off
	pip install -r test-requirements.txt --progress-bar off

lint-fix:
	select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	autopep8 --in-place --recursive --max-line-length=100 --select=${select} ci
	isort --recursive ci

lint-tests:
	flake8 ci
	isort --check-only --recursive ci

unit-tests:
	pytest ci/test --cov=ci --cache-clear --show-capture=stderr --disable-warnings -vv \
	--circle-token ${CIRCLE_TOKEN} --github-token ${GITHUB_TOKEN}
