.PHONY: print-env \
        init \
        install \
        install-update \
        install-package \
        virtualenv \
        bower \
        clean \
        local-settings \
        deploy \
        manage \
        migrations \
        migrate \
        run \
        restart \
        shell \
        test \
        coverage \

.DEFAULT_GOAL := run

PROJECT_NAME = campusmap
VENV_DIR ?= .env
BIN_DIR = $(VENV_DIR)/bin
PYTHON = $(BIN_DIR)/python
PIP = $(BIN_DIR)/pip
MANAGE = $(PYTHON) manage.py
SETTINGS_MODULE = $(DJANGO_SETTINGS_MODULE)
ifeq ($(strip $(SETTINGS_MODULE)),)
SETTINGS_MODULE = $(PROJECT_NAME).settings
endif
TEST_LOCAL_SETTINGS_FILE = local.base.cfg\#test

print-env:
	@echo PROJECT_NAME: $(PROJECT_NAME)
	@echo VENV_DIR: $(VENV_DIR)
	@echo BIN_DIR: $(BIN_DIR)
	@echo PYTHON: $(PYTHON)
	@echo PIP: $(PIP)
	@echo MANAGE: $(MANAGE)
	@echo SETTINGS_MODULE: $(SETTINGS_MODULE)

init:
	@$(MAKE) virtualenv args='-p python3'
	@$(MAKE) test

install:
	$(PIP) install -r requirements.txt

install-update:
	$(PIP) install -U -r requirements.txt

# pip install $(args)
# Examples:
#     make install-package args=bpython
#     make install-package args='pep8 pyflakes'
#     make install-package args='-U pep8'
install-package:
	$(PIP) install $(args)

virtualenv:
	@if [ -d "$(VENV_DIR)" ]; then \
	    echo "Directory exists: $(VENV_DIR)"; \
	    exit 1; \
	fi
	virtualenv $(args) $(VENV_DIR)
	@echo
	$(MAKE) install

bower:
	cd $(PROJECT_NAME)/static && bower install

clean:
	find . -iname '*.pyc' -delete
	find . -iname '*.pyo' -delete
	find . -iname '__pycache__' -print0 | xargs -0 rm -rf

local-settings:
	@echo "Loading settings module: $(SETTINGS_MODULE)"
	$(BIN_DIR)/make-local-settings $(or $(strip $(env)),dev)

env ?= stage
deploy:
	$(BIN_DIR)/invoke -e $(env) deploy --delete

## Django (wrappers for ./manage.py commands)

# Run a manage.py command
#
# This is here so we don't have to create a target for every single manage.py
# command. Of course, you could also just source your virtualenv's bin/activate
# script and run manage.py directly, but this provides consistency if you're in
# the habit of using make.
#
# Examples:
#     make manage args=migrate
#     make manage args='runserver 8080'
manage:
	@$(MANAGE) $(args)

migrations:
	$(MANAGE) makemigrations $(for)

migrate:
	$(MANAGE) migrate

# Run the django web server
host ?= 0.0.0.0
port ?= 8000
run:
	$(MANAGE) runserver $(host):$(port)

restart:
	touch $(PROJECT_NAME)/wsgi.py

# Start a django shell
# Run `make install-package name=bpython` (or ipython) first if you want
# a fancy shell
shell:
	$(MANAGE) shell $(args)

# Run the unit tests
# Use `make test test=path.to.test` to run a specific test
test:
	LOCAL_SETTINGS_FILE=$(TEST_LOCAL_SETTINGS_FILE) $(MANAGE) test $(test)

# Run unit tests then print a coverage report
coverage:
	LOCAL_SETTINGS_FILE=$(TEST_LOCAL_SETTINGS_FILE) $(BIN_DIR)/coverage run --source=$(PROJECT_NAME) manage.py test
	$(BIN_DIR)/coverage report

## /Django
