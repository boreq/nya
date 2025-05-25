.PHONY: dev
dev:
	docker compose -f compose.dev.yaml up --build

.PHONY: venv
venv:
	rm -rf ./venv
	python -m venv venv
	source ./venv/bin/activate && pip install pyflakes

.PHONY: pyflakes
pyflakes:
	source ./venv/bin/activate && pyflakes nya

.PHONY: static
static:
	sh build_static
