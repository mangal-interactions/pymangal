python = python2
pip = pip2

all: requirements test install

requirements: requirements.txt
	$(pip) install -r requirements.txt

test:
	$(python) test_pymangal.py

install:
	$(python) setup.py install

