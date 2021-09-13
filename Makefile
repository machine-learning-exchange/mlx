# Copyright 2021 IBM Corporation
#
# SPDX-License-Identifier: Apache-2.0

# Acknowledgements:
#  - The help target was derived from https://stackoverflow.com/a/35730328/5601796

.PHONY: help
help: ## Display the Make targets
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

.PHONY: check_doc_links
check_doc_links: ## Check Markdown files for valid links
	@pip3 show requests > /dev/null || pip3 install requests
	@python3 tools/python/verify_doc_links.py
	@echo "$@: OK"
