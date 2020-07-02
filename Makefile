install:
	pip install -r requirements.txt --progress-bar off
	pip install -r test-requirements.txt --progress-bar off

lint-fix:
	select="E225,E303,E302,E203,E128,E231,E251,E271,E127,E126,E301,W291,W293,E226,E306,E221"
	autopep8 --in-place --recursive --max-line-length=100 --select=${select} circleci
	isort --recursive circleci

lint-tests:
	flake8 circleci
	isort --check-only --recursive circleci

unit-tests:
	pytest -s circleci/test.py --cov=circleci --circle-token ${CIRCLE_TOKEN} \
	--cache-clear --show-capture=stderr --disable-warnings -vv
