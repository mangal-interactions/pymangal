python = python
pip = pip

all: requirements test install

requirements: requirements.txt
	$(pip) install -r requirements.txt

test:
	$(python) tests.py

.version: .tag pymangal/__init__.py
	@python .makeversion.py 1>/dev/null 2>/dev/null

.tag:
	@git tag | tail -n 1 > .tag

setup.py: .tag .version .makesetup.py
	@python .makesetup.py

install: setup.py
	$(python) $< $@
