#
# Development by Carl J. Nobile
#

PREFIX		= $(shell pwd)
PACKAGE_DIR	= $(shell echo $${PWD\#\#*/})
DOCS_DIR	= $(PREFIX)/docs
TODAY		= $(shell date +"%Y-%m-%d_%H%M")
RM_REGEX	= '(^.*.pyc$$)|(^.*.wsgic$$)|(^.*~$$)|(.*\#$$)|(^.*,cover$$)'
RM_CMD		= find $(PREFIX) -regextype posix-egrep -regex $(RM_REGEX) \
                  -exec rm {} \;
PIP_ARGS	=

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="dist/*" $(PACKAGE_DIR))

docs: clean
	@(cd $(DOCS_DIR); make)

.PHONY	: build
build	: clean
	python setup.py sdist

.PHONY	: upload
upload	: clobber
	python setup.py sdist upload -r pypi

.PHONY	: upload-test
upload-test: clobber
	python setup.py sdist upload -r pypitest

.PHONY	: install-dev
install-dev:
	pip install $(PIP_ARGS) -r requirements.txt

.PHONY	: install-prd
install-prd:
	pip install $(PIP_ARGS) -r requirements.txt

.PHONY	: install-stg
install-stg:
	pip install $(PIP_ARGS) -r requirements.txt

#----------------------------------------------------------------------

clean	:
	$(shell $(RM_CMD))

clobber	: clean
	@rm -rf *.egg-info
	@rm -rf dist
