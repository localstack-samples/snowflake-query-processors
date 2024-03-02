VENV_BIN = python3 -m venv
VENV_DIR ?= .venv
VENV_ACTIVATE = $(VENV_DIR)/bin/activate
VENV_RUN = . $(VENV_ACTIVATE)
TEST_PATH ?= tests
PYTEST_ARGS ?= --log-cli-level=INFO

usage:				## Shows usage for this Makefile
	@cat Makefile | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

venv: $(VENV_ACTIVATE)

$(VENV_ACTIVATE): setup.py setup.cfg
	test -d .venv || $(VENV_BIN) .venv
	$(VENV_RUN); pip install --upgrade pip setuptools plux
	$(VENV_RUN); pip install -e .
	touch $(VENV_DIR)/bin/activate

clean:				## Clean the project
	rm -rf .venv/
	rm -rf build/
	rm -rf .eggs/
	rm -rf *.egg-info/
	rm -rf dist/

install: venv		## Install packages in the virtual environment
	$(VENV_RUN); python setup.py develop; pip install -e .[dev,test]

dist: venv			## Build the distribution
	$(VENV_RUN); python setup.py sdist

lint:				## Run code linter to check code style
	$(VENV_RUN); pflake8 --show-source snowflake_ext tests

format:				## Run black and isort code formatter
	$(VENV_RUN); black .; isort .

test:				## Run tests
	$(VENV_RUN); pytest -sv $(PYTEST_ARGS) $(PYTEST_XDIST_ARGS) $(TEST_PATH)

build:          	## Build the extension
	mkdir -p build/
	cp -r setup.py setup.cfg README.md snowflake_ext build/
	(cd build && python setup.py sdist)

start:            	## Start LocalStack in extensions dev mode
	$(VENV_RUN); IMAGE_NAME=localstack/snowflake DOCKER_FLAGS='-e DEBUG_PLUGINS=1 -e SF_LOG=trace'"$(DOCKER_FLAGS)" DEBUG=1 EXTENSION_DEV_MODE=1 localstack start

stop:            	## Stop the Running LocalStack container
	$(VENV_RUN); localstack stop

enable-dev: build   ## Enable the extension in LocalStack in dev mode
	localstack extensions dev enable .

disable-dev: build   ## Disable the extension in LocalStack in dev mode
	localstack extensions dev disable .

enable: $(wildcard ./build/dist/localstack-snowflake-hello-world-*.tar.gz)	## Enable/install the extension in LocalStack
	$(VENV_RUN); \
		pip uninstall --yes localstack-snowflake-hello-world; \
		localstack extensions uninstall localstack-snowflake-hello-world; \
		localstack extensions -v install file://./$?

.PHONY: clean dist install publish lint format build test start stop logs enable enable-dev
