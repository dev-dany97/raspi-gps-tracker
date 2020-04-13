# version: 1.0.0
.PHONY: all test coverage pep8

all: test

pep8:
	pycodestyle --ignore E402,E501 .

test:
	@python -m unittest discover

coverage:
	@python -m coverage run --branch --source ../../src -m unittest discover
	@python -m coverage report -m

combine_coverage:
	@python -m coverage combine -a ../integrationtest_auto/.coverage
	@python -m coverage html
	@python -m coverage xml
