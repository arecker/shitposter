.phony: all
all: run

.phony: run
run: venv/bin/python
	./shitposter.py

venv/bin/python:
	python -m venv ./venv
	./venv/bin/pip install -q --upgrade pip
	./venv/bin/pip install -q feedparser
	./venv/bin/pip install -q slack-sdk
	./venv/bin/pip install -q tweepy
	./venv/bin/pip install -q selenium
	./venv/bin/pip install -q Mastodon.py

.phony: clean
clean:
	rm -rf ./venv
