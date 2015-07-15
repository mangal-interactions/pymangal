python = python
pip = pip

all: requirements test install

requirements: requirements.txt
	$(pip) install -r requirements.txt

test:
	$(python) tests.py

.version: pymangal/__init__.py
	@python .makeversion.py 1>/dev/null 2>/dev/null

.tag: .version
	@git tag | tail -n 1 > .tag

setup.py: test


install: setup.py
	$(python) $< $@
