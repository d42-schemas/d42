PROJECT_NAME=d42

.PHONY: install
install:
	poetry install

.PHONY: build
build:
	poetry build

.PHONY: publish
publish:
	poetry publish

.PHONY: test
test:
	poetry run python -m unittest discover .

.PHONY: check-imports
check-imports:
	poetry run python -m isort ${PROJECT_NAME} tests --check-only

.PHONY: sort-imports
sort-imports:
	poetry run python -m isort ${PROJECT_NAME} tests

.PHONY: lint
lint: check-imports

.PHONY: bump
bump:
	bump2version $(filter-out $@,$(MAKECMDGOALS))
	@git --no-pager show HEAD
	@echo
	@git verify-commit HEAD
	@git verify-tag `git describe`
	@echo
	# git push origin master --tags
%:
	@:
