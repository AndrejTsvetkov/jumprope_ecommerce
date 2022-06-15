TESTS = tests

VENV ?= .venv
CODE = tests app

BIN_PATH = bin

ifeq ($(OS), Windows_NT)
	BIN_PATH = Scripts
endif

.PHONY: help
help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


.PHONY: venv
venv:
	python3.9 -m venv $(VENV)
	$(VENV)/$(BIN_PATH)/python -m pip install --upgrade pip
	$(VENV)/$(BIN_PATH)/python -m pip install poetry
	$(VENV)/$(BIN_PATH)/poetry install

.PHONY: test
test: ## Runs pytest
	$(VENV)/$(BIN_PATH)/pytest -v tests

.PHONY: lint
lint: ## Lint code
	$(VENV)/$(BIN_PATH)/flake8 --jobs 4 --statistics --show-source $(CODE)
	$(VENV)/$(BIN_PATH)/pylint --jobs 4 --rcfile=setup.cfg $(CODE)
	$(VENV)/$(BIN_PATH)/mypy $(CODE)
	$(VENV)/$(BIN_PATH)/black --skip-string-normalization --check $(CODE)

.PHONY: format
format: ## Formats all files
	$(VENV)/$(BIN_PATH)/isort $(CODE)
	$(VENV)/$(BIN_PATH)/black --skip-string-normalization $(CODE)
	$(VENV)/$(BIN_PATH)/autoflake --recursive --in-place --remove-all-unused-imports $(CODE)
	$(VENV)/$(BIN_PATH)/unify --in-place --recursive $(CODE)

.PHONY: ci
ci:	lint test ## Lint code then run tests

.PHONY: init_db
init_db:
	$(VENV)/$(BIN_PATH)/python init_db.py

.PHONY: up
up:
	docker-compose up -d --build

# only for docker
.PHONY: app
app:
	uvicorn app.main:app --host=0.0.0.0 --port=80

.PHONY: admin
admin:
	flask run --host=0.0.0.0 --port=5000
