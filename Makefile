#
# Development by Carl J. Nobile
#

PREFIX		= $(shell pwd)
PACKAGE_DIR	= $(shell echo $${PWD\#\#*/})
DOCS_DIR	= $(PREFIX)/docs
TODAY		= $(shell date +"%Y-%m-%d_%H%M")
PIP_ARGS	=

#----------------------------------------------------------------------
all	: tar

#----------------------------------------------------------------------
tar	: clean
	@(cd ..; tar -czvf $(PACKAGE_DIR).tar.gz --exclude=".git" \
          --exclude="logs/*.log" --exclude="dist/*" $(PACKAGE_DIR))

api-docs: clean
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
	$(shell cleanDirs.sh clean)
	@rm -rf *.egg-info
	@rm -rf dist
	#@rm -rf python-forensics-1.0

clobber	: clean
	@(cd $(DOCS_DIR); make clobber)
	@rm logs/*.log
