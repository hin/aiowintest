all: test

.PHONY: test
test:
	python setup.py pytest

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
