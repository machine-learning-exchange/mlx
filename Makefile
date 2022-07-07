# Copyright 2021-2022 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# Acknowledgements:
#  - The help target was derived from https://stackoverflow.com/a/35730328/5601796

VENV ?= .venv
export VIRTUAL_ENV := $(abspath ${VENV})
export PATH := ${VIRTUAL_ENV}/bin:${PATH}
GITHUB_ACTION ?= false

.PHONY: help
help: ## List the Make targets with description
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.PHONY: venv
venv: $(VENV)/bin/activate ## Create and activate Python virtual environment
$(VENV)/bin/activate: api/client/setup.py api/server/setup.py api/server/requirements.txt
# create/update the VENV when there was a change to setup.py or requirements.txt
# check if api server or client is already installed (Travis/CI did during install step)
# use pip from the specified VENV as opposed to any pip available in the shell
	@echo "VENV=$(VENV)"
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(VENV)/bin/pip show mlx-api >/dev/null 2>&1 || $(VENV)/bin/pip install -e api/server && $(VENV)/bin/pip install -r api/server/requirements.txt
	@$(VENV)/bin/pip show mlx-client >/dev/null 2>&1 || $(VENV)/bin/pip install -e api/client && $(VENV)/bin/pip install -r api/client/requirements.txt
	@if [ "$(GITHUB_ACTION)" = "false" ]; then touch $(VENV)/bin/activate; fi

.PHONY: install
install: venv ## Install Python packages in a virtual environment
	@echo "Run 'source $(VENV)/bin/activate' to activate the virtual environment."

.PHONY: check_npm_packages
check_npm_packages: ## Verify NPM packages
	@python3 tools/python/verify_npm_packages.py --verify
	@echo "$@: OK"

.PHONY: update_npm_packages
update_npm_packages: ## Update NPM packages
	@python3 tools/python/verify_npm_packages.py --update
	@echo "$@: OK"

.PHONY: check_doc_links
check_doc_links: ## Check markdown files for invalid links
	@pip3 show requests > /dev/null || pip3 install requests
	@python3 tools/python/verify_doc_links.py
	@echo "$@: OK"

.PHONY: update_doc_table
update_doc_table: ## Regenerate the /docs/README.md file
	@python3 tools/python/update_doc_table.py
	@echo "$@: OK"

.PHONY: check_license
check_license: ## Make sure source files have license header
	@git grep -L "SPDX-License-Identifier: Apache-2.0" -- *.py *.yml *.yaml *.sh *.html *.js *.css *.ts *.tsx ':!*.bundle.js' | \
		grep . && echo "Missing license headers in files above. Run './tools/bash/add_license_headers.sh'" && exit 1 || \
		echo "$@: OK"

.PHONY: lint_python
lint_python: venv ## Check Python code style compliance
	@which flake8 > /dev/null || pip install flake8
	@flake8 api/server api/client tools/python --show-source --statistics \
		--select=E9,E2,E3,E5,F63,F7,F82,F4,F841,W291,W292 \
		--per-file-ignores api/server/swagger_server/controllers/*,api/server/swagger_server/models/*,api/client/swagger_client/models/*,api/client/test/*:E252,F401,W291 \
		--exclude .git,__pycache__,docs/source/conf.py,old,build,dist,venv \
		--max-line-length=140
	@echo "$@: OK"

.PHONY: lint_javascript
lint_javascript: ## Check Javascript code style compliance
	@cd dashboard/origin-mlx && npm run lint:fix
	@echo "$@: OK"

.PHONY: lint
lint: lint_javascript lint_python ## Check for code style violations (JavaScript, Python)
	@echo "$@: OK"
