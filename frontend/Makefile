package = campusmap

BUILD_DIR := build

CSS_C := ./node_modules/.bin/node-sass
CSS_C_FLAGS := --source-map true --source-map-contents
CSS_SRC := $(package)
CSS_SRC_FILES := $(shell find $(CSS_SRC) -type f -name 'main.scss')
CSS_INC_FILES := $(shell find $(CSS_SRC) -type f -name '*.scss' -not -name 'main.scss')
CSS_OUT := $(BUILD_DIR)/$(CSS_SRC)/css
CSS_TARGETS := $(patsubst $(CSS_SRC)/%.scss, $(CSS_OUT)/%.css, $(CSS_SRC_FILES))

JS_C := ./node_modules/.bin/r.js
JS_C_FLAGS := -o
JS_C_OPT_BASE_URL := baseUrl=$(PWD)
JS_C_OPT_MAIN_CONFIG_FILE := mainConfigFile=$(PWD)/requireConfig.js
JS_C_OPT_OPTIMIZE := optimize=uglify
JS_C_OPT_PATHS := paths.ol=empty:
JS_C_OPTS := $(JS_C_OPT_BASE_URL) $(JS_C_OPT_MAIN_CONFIG_FILE)
JS_C_OPTS += $(JS_C_OPT_OPTIMIZE) $(JS_C_OPT_PATHS)
JS_SRC := $(package)
JS_SRC_FILES := $(shell find $(JS_SRC) -type f -name 'main.js')
JS_INC_FILES := $(shell find $(JS_SRC) -type f -name '*.js' -not -name 'main.js')
JS_INC_FILES += $(shell find $(JS_SRC) -type f -name '*.html')
JS_OUT := $(BUILD_DIR)/$(JS_SRC)/js
JS_TARGETS := $(patsubst $(JS_SRC)/%, $(JS_OUT)/%, $(JS_SRC_FILES))

VENV ?= .env
VENV_PYTHON ?= python3.6

init: $(VENV) node_modules css js
reinit: clean-build init

node_modules: package.json
	npm install

$(VENV):
	virtualenv -p $(VENV_PYTHON) $(VENV)
	$(VENV)/bin/pip install -r requirements.txt

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

css: node_modules $(CSS_TARGETS)

$(CSS_OUT): $(BUILD_DIR)
	mkdir -p $(CSS_OUT)

# $< = source SCSS file
# $@ = compiled CSS file
$(CSS_TARGETS): $(CSS_OUT)/%.css : $(CSS_SRC)/%.scss $(CSS_INC_FILES) | $(CSS_OUT)
	$(CSS_C) $(CSS_C_FLAGS) $< $@

js: node_modules $(JS_TARGETS)

$(JS_OUT): $(BUILD_DIR)
	mkdir -p $(JS_OUT)

# $< = source JS file
# $@ = compiled JS file
$(JS_TARGETS): $(JS_OUT)/%.js : $(JS_SRC)/%.js $(JS_INC_FILES) | $(JS_OUT)
	$(JS_C) $(JS_C_FLAGS) $(JS_C_OPTS) name=$< out=$(PWD)/$@

run: init
	@$(VENV)/bin/runcommand dev-server

env ?= stage
deploy: init
	@$(VENV)/bin/runcommand -E -e $(env) -v $(shell git rev-parse --short HEAD) deploy

clean-all: clean-build
	rm -rf node_modules
clean-build: clean-css clean-js
	rm -rf build
clean-css:
	rm -f $(CSS_TARGETS)
	rm -rf $(CSS_OUT)
clean-js:
	rm -f $(JS_TARGETS)
	rm -rf $(JS_OUT)

.PHONY := init css js run deploy clean-all clean-build clean-css clean-js
