python = python
pip = pip

all: requirements test install

requirements: requirements.txt
	$(pip) install -r requirements.txt

test:
	$(python) tests.py

install:
	$(python) setup.py install
