#
# Copyright 2015 Michael Sparks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
PYTHON=`which python`
DESTDIR=/
PROJECT=pyxie
VERSION=0.0.16

all:
	@echo "make source - Create source package"
	@echo "make install - Install on local system (only during development)"
	@echo "make deb - Generate a deb package - for local testing"
	@echo "make ppadeb - Generate files necessary to trigger build on PPA"
	@echo "make use - use the locally generate deb for local testing"
	@echo "make purge - uninstall the locally generate deb"
	@echo "make clean - Clean up directories"
	@echo "make distclean - Like make clean, but also remote dist directory"
	@echo "make devlopp - purge, distclean, make deb, use deb"
	@echo "make test - run behave and other tests"
	@echo "make clean - Get rid of scratch and byte files"
	@echo "make test - Run any unit tests"

source:
	$(PYTHON) setup.py sdist $(COMPILE)

install:
	$(PYTHON) setup.py install --root $(DESTDIR) $(COMPILE)

deb:
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -uc -us

ppadeb:
	python setup.py sdist
	cd dist && py2dsc $(PROJECT)-* && cd deb_dist/$(PROJECT)-$(VERSION) && debuild -S && cd .. && dput ppa:sparkslabs/packages $(PROJECT)_*_source.changes
	@echo "Clean up dist before uploading to pypi, or it'll contain too much junk"

use:
	sudo dpkg -i dist/deb_dist/python-$(PROJECT)*deb

purge:
	sudo apt-get purge python-$(PROJECT)

clean:
	$(PYTHON) setup.py clean
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
	rm -f parser.out parsetab.py

distclean:
	$(PYTHON) setup.py clean
	rm -rf dist
	rm -rf build/ MANIFEST
	find . -name '*.pyc' -delete
	rm -f parser.out parsetab.py

devloop: purge distclean deb use
	echo

test:
	PYTHONPATH="." ./bin/pyxie --test run-tests
	# behave
