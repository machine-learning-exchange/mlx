# Copyright 2021 The MLX Contributors
#
# SPDX-License-Identifier: Apache-2.0

# Acknowledgements:
#  - The help target was derived from https://stackoverflow.com/a/35730328/5601796

.PHONY: help
help: ## List the Make targets with description
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.PHONY: check_doc_links
check_doc_links: ## Check markdown files for invalid links
	@pip3 show requests > /dev/null || pip3 install requests
	@python3 tools/python/verify_doc_links.py
	@echo "$@: OK"

.PHONY: check_license
check_license: ## Make sure source files have license header
	@git grep -L "SPDX-License-Identifier: Apache-2.0" -- *.py *.yml *.yaml *.sh *.html *.js *.css *.ts *.tsx ':!*.bundle.js' | \
		grep . && echo "Missing license headers in files above. Run './tools/bash/add_license_headers.sh'" && exit 1 || \
		echo "$@: OK"
