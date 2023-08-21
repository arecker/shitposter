.phony: all
all: run

.phony: run
run: venv/bin/python
	./shitposter.py

venv/bin/python: requirements.txt
	python -m venv --copies ./venv
	./venv/bin/pip install -q --upgrade pip
	./venv/bin/pip install -q -r requirements.txt

.phony: clean
clean:
	rm -rf ./venv
