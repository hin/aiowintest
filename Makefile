all: test

.PHONY: test
test:
	coverage run --source aiowintest -m pytest
	coverage report
	coverage html

.PHONY: dist
dist:
	rm -f dist/*
	python setup.py sdist bdist_wheel

.PHONY: docs
docs:
	sphinx-build docs docs/_build

.PHONY: upload
upload: dist
	twine upload dist/*
