# vim:ts=8:sw=8:noet

SPHINX_BUILD	?= env PYTHONPATH=.. sphinx-build
SPHINX_OPTS	?=
SPHINX_SOURCE	= source
SPHINX_DEST	= build

.PHONY:	Makefile apidoc cibuild help install-reqs

help:
	$(SPHINX_BUILD) -M help $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)

apidoc:
	sphinx-apidoc --force --output-dir $(SPHINX_SOURCE) ../letsdns
	rm $(SPHINX_SOURCE)/modules.rst
	sed -i'' -E -e 's/:(undoc-members:)/:no-\1/g' $(SPHINX_SOURCE)/*.rst

cibuild:	install-reqs apidoc html

install-reqs:
	pip install -r ../requirements.txt


%:	Makefile
	$(SPHINX_BUILD) -M $@ $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)
