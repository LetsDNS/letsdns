# vim:ts=4:sw=4:noet

RSYNC_OPTS		?= --compress --delete --ipv6 --recursive --rsh=ssh --times --verbose
SED_INPLACE		?= /opt/local/bin/gsed -i''
SPHINX_BUILD	?= env PYTHONPATH=.. sphinx-build
SPHINX_OPTS		?=
SPHINX_DEST		= build
SPHINX_SOURCE	= source

.PHONY:	Makefile apidoc cibuild help install-reqs publish

help:
	$(SPHINX_BUILD) -M help $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)

apidoc:
	sphinx-apidoc --force --output-dir $(SPHINX_SOURCE) ../letsdns
	rm $(SPHINX_SOURCE)/modules.rst
	$(SED_INPLACE) -E -e 's/:(undoc-members:)/:no-\1/g' $(SPHINX_SOURCE)/*.rst

cibuild:	install-reqs apidoc html

install-reqs:
	pip install -r ../requirements.txt

publish:
	rsync $(RSYNC_OPTS) $(SPHINX_DEST)/html/ letsdns.org:/var/www/letsdns

%:	Makefile
	$(SPHINX_BUILD) -M $@ $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)
