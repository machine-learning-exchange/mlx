# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# Acknowledgements:
#  - The help target was derived from https://stackoverflow.com/a/35730328/5601796

.PHONY: help
help: ## List the Make targets with description
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

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
	@which flake8 > /dev/null || pip install flake8 || pip3 install flake8
	@flake8 . --show-source --statistics \
		--select=E9,E2,E3,E5,F63,F7,F82,F4,F841,W291,W292 \
		--per-file-ignores ./*:F841 \
		--exclude .git,__pycache__,docs/source/conf.py,old,build,dist,venv \
		--max-line-length=140
	@echo "$@: OK"

.PHONY: lint_javascript
lint_javascript: ## Check Javascript code style compliance
	@cd dashboard/origin-mlx && npm run lint -- --fix
	@echo "$@: OK"
