package = campusmap

venv ?= .env
venv_python ?= python3.6
bin = $(venv)/bin
site_packages = $(venv)/lib/$(venv_python)/site-packages

arctasks = $(site_packages)/arctasks
arctasks_url = https://github.com/PSU-OIT-ARC/arctasks/archive/master.tar.gz#egg=psu.oit.arc.tasks

init: $(venv) $(arctasks) local.dev.cfg local.test.cfg
	$(bin)/runcommand init

reinit: clean-egg-info clean-pyc clean-venv init

$(venv):
	virtualenv -p $(venv_python) $(venv)

install: $(venv)
	$(bin)/pip install -r requirements.txt
reinstall: clean-egg-info clean-pyc install

install-arctasks: $(arctasks)
reinstall-arctasks: clean-arctasks $(arctasks)

$(arctasks):
	$(bin)/pip install -f https://pypi.research.pdx.edu/dist/ $(arctasks_url)

local.dev.cfg:
	echo '[dev]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

local.test.cfg:
	echo '[test]' >> $@
	echo 'extends = "local.base.cfg"' >> $@

test:
	$(bin)/runcommand test

run:
	$(bin)/runcommand runserver

to ?= stage
deploy:
	$(bin)/runcommand --echo --env $(to) deploy

clean: clean-pyc
clean-all: clean-build clean-dist clean-egg-info clean-pyc clean-static clean-venv
clean-arctasks:
	pip uninstall -y psu.oit.arc.tasks
clean-build:
	rm -rf build
clean-dist:
	rm -rf dist
clean-egg-info:
	rm -rf *.egg-info
clean-pyc:
	find . -name __pycache__ -type d -print0 | xargs -0 rm -r
	find . -name '*.py[co]' -type f -print0 | xargs -0 rm
clean-venv:
	rm -rf $(venv)

.PHONY = init reinit install reinstall test run deploy \
         clean clean-all clean-arctasks clean-build clean-dist clean-egg-info clean-node_modules \
         clean-pyc clean-venv
