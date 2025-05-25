.PHONY: dev
dev:
	docker compose -f compose.dev.yaml up --build

.PHONY: venv
venv:
	rm -rf ./venv
	python -m venv venv
	source ./venv/bin/activate && pip install -e .

.PHONY: run
run:
	source ./venv/bin/activate && flask --app nya run

.PHONY: pyflakes
pyflakes:
	pyflakes nya

.PHONY: test
test:
	py.test tests

.PHONY: static
static:
	sh build_static
