package = campusmap

VENV ?= .env
VENV_PYTHON ?= python3.6

init: $(VENV) node_modules
reinit: clean-all init

$(VENV):
	virtualenv -p $(VENV_PYTHON) $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

node_modules: package.json
	npm install

run:
	npm start

env ?= stage
deploy: init
	@$(VENV)/bin/runcommand -E -e $(env) -v $(shell git rev-parse --short HEAD) deploy

clean-all: clean-npm clean-venv
clean-npm:
	rm -rf node_modules
clean-venv:
	rm -rf $(VENV)

.PHONY := init reinit run deploy clean-all clean-npm clean-venv
