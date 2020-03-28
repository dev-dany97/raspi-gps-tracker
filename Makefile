# version: 1.0.0
include Makefile_toolchain
.PHONY: help all

btp := "./build_temp_path"
drp := "./dist"

all: help

#
# LINTERS AND CODESTYLE TARGETS
#
.PHONY: pep8 pylint
help::
	@echo pylint - run pylint over the source files and print the result.
pylint:
	@"$(MAKE)" linter

help::
	@echo pylint - run pylint over the source files and print the result.
linter:
	@echo ">> run pylint check"
	@python pylint_test.py

help::
	@echo pep8 - run pep8 test over the source files and print the result.
pep8:
	pycodestyle --ignore E402,E501 --exclude=docs,venv .

#
# TEST AND COVERAGE TARGETS
#
.PHONY: test coverage
help::
	@echo test - run unit tests.
test:
	@"$(MAKE)" -C test

help::
	@echo coverage - create a coverage report by running all available tests.
coverage:
	@"$(MAKE)" -C test coverage
	@echo You can also find a HTML report under "test/unittest/htmlcov/index.html"

#
# DOCUMENTATION TARGETS
#
.PHONY: docs sphinx sphinx_versioning
help::
	@echo docs - build the documentation for the project. Once this step finishes a html documentation will be available under "dist/docs_html".
docs:
	sphinx-apidoc -f -o $(btp) ./src/
	@cp -R docs/* $(btp)
	@"$(MAKE)" -C $(btp) html
	@-rm -rf $(drp)/docs_html
	@-mkdir $(drp)
	@-mkdir $(drp)/docs_html
	@cp -R $(btp)/_build/html/* $(drp)/docs_html
	@rm -rf $(btp)

help::
	@echo sphinx_versioning - build the documentation for the project by using the sphinx-versioning module. Once this step finishes a html documentation for ALL version tags will be available under "dist/docs_html".
sphinx_versioning:
	sphinx-versioning build --whitelist-branches 'version_*' -T docs $(btp)/docs
	@-rm -rf $(drp)/docs_html
	@-mkdir $(drp)
	@-mkdir $(drp)/docs_html
	@cp -R $(btp)/docs/* $(drp)/docs_html
	@rm -rf $(btp)

#
# PACKAGE BUILDING TARGETS
#
.PHONY: package publish executable zip_executable
help::
	@echo package - build a package which can be installed via pip. See the wiki how to upload a package so that others can easily install it via pip. The built package can be found locally in the "dist/pip" folder.
package:
	@python setup.py build -b $(btp) egg_info -e $(btp) bdist_wheel -b $(btp) -d $(drp)/pip --universal

help::
	@echo publish - build and publish a package
publish:
	@python setup.py build -b $(btp) egg_info -e $(btp) bdist_wheel -b $(btp) -d $(drp)/pip --universal upload -r intence

help::
	@echo executable - build a standalone executable. The built executable can be found under "dist/standalone_exe".
executable:
	@"$(MAKE)" version_file
	@"$(MAKE)" version_module
	@-mkdir $(btp)
	@pyinstaller --specpath $(btp) --onefile --distpath $(drp)/standalone_exe src/dany_raspi_gps_tracker
	@"$(MAKE)" zip_executable
	@-rm -rf $(btp)
