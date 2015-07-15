python = python
pip = pip

all: requirements test install

requirements: requirements.txt
	$(pip) install -r requirements.txt

test:
	$(python) tests.py

.tag:
	@git tag | tail -n 1 > .tag

.version: .tag pymangal/__init__.py
	@python .makeversion.py 1>/dev/null 2>/dev/null

setup.py: .version .makesetup.py
	@python .makesetup.py

pypitest: setup.py
	$(python) $< register -r pypitest
	$(python) $< sdist upload -r pypitest

pypilive: setup.py
	$(python) $< register -r pypi
	$(python) $< sdist upload -r pypi

install: setup.py
	$(python) $< $@
