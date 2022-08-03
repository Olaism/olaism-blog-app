setup:
	python3 -m venv venv

install:
	pip install -r requirements.txt

test:
	python -m pytest -vv --cov=myreoplib tests/*.py

lint:
	pylint --disable=R,C config cli web

format:
	python -m black config/*.py

git-add:
	git add .

git-push-master:
	git push -u origin master