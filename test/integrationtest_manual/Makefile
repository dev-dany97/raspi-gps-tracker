# version: 1.0.0
.PHONY: all test coverage pep8

all: test

pep8:
	pycodestyle --ignore E402,E501 .

test:
	@echo TODO: add your description here

# NOTE: this coverage target is not called from the test/Makefile
coverage:
	@python -m coverage run --branch --source ../../src -m unittest discover
	@python -m coverage report -m
	@python -m coverage html
