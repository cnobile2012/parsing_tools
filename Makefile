#
# Development by Carl J. Nobile
#
include include.mk

PREFIX		= $(shell pwd)
BASE_DIR	= $(shell echo $${PWD\#\#*/})
PACKAGE_DIR	= $(BASE_DIR)-$(VERSION)
DOCS_DIR	= $(PREFIX)/docs
TODAY		= $(shell date +"%Y-%m-%d_%H%M")
RM_REGEX	= '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;
COVERAGE_FILE	= $(PREFIX)/.coveragerc
PIP_ARGS	=
TEST_PATH	= # The path to run tests on.

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="dist/*" $(PACKAGE_DIR))

docs: clean
	@(cd $(DOCS_DIR); make)

.PHONY	: build
build	: clobber
	@./config.py
	hatch build dist

.PHONY	: upload
upload	: clobber
	@./config.py
	hatch publish --repo main dist/*

.PHONY	: upload-test
upload-test: clobber
	@./config.py
	hatch publish --repo test dist/*

.PHONY	: install-dev
install-dev:
	pip install $(PIP_ARGS) -r requirements/development.txt

#----------------------------------------------------------------------
# Run all tests
# $ make tests
#
# Run all tests in a specific test file.
# $ make tests TEST_PATH=tests/test_bases.py
#
# Run all tests in a specific class within a test file.
# $ make tests TEST_PATH=tests/test_bases.py::TestBases
#
# Run just one test in a specific class within a test file.
# $ make tests TEST_PATH=tests/test_bases.py::TestBases::test_version
.PHONY	: tests flake8
tests	: clobber
	@rm -rf $(DOCS_DIR)/htmlcov
	@coverage erase --rcfile=$(COVERAGE_FILE)
	@coverage run --rcfile=$(COVERAGE_FILE) -m pytest tests --capture=tee-sys \
        $(TEST_PATH)
	@coverage report -m --rcfile=$(COVERAGE_FILE)
	@coverage html --rcfile=$(COVERAGE_FILE)
	@echo $(TODAY)

flake8  :
	# Error on syntax errors or undefined names.
	flake8 . --select=E9,F7,F63,F82 --show-source
	# Warn on everything else.
	flake8 . --exit-zero

#----------------------------------------------------------------------

clean	:
	$(shell $(RM_CMD))

clobber	: clean
	@rm -rf *.egg-info
	@rm -rf dist
	@rm -rf $(DOCS_DIR)/htmlcov
