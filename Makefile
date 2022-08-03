setup:
	pipenv install -r requirements.txt
	pipenv shell

install:
	pip install -r requirements.txt

test:
	python manage.py test

validate-circleci:
	circleci config validate

run-circleci-local:
	circleci local execute

lint:
	docker run --rm -i hadolint/hadolint < Dockerfile
	pylint --disable=R,C config manage.py

format:
	python -m black config/*.py

git-push:
	git add .
	git commit -m ${message}
	git push -u origin master