.PHONY: help setup lint format test

help: ## Display this help message
	@echo "Available commands:"
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort

setup: ## Set up the project using poetry
	poetry install

lint: ## Run pylint with the specified parameters
	poetry run pylint --disable=all --enable=unused-import zentunes

format: ## Format the code using black
	poetry run black zentunes

test: ## Run the tests using pytest
	poetry run pytest

