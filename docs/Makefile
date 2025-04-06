# vim: ts=4 sw=4 noet

RSYNC_OPTS		?= --compress --delete --ipv6 --recursive --rsh=ssh --times --verbose
SED_IE			?= sed -i "" -E
SPHINX_BUILD	?= env PYTHONPATH=.. sphinx-build
SPHINX_OPTS		?=
SPHINX_DEST		= build
SPHINX_SOURCE	= source

define usage

Available make targets are:

  apidoc   Generate API documentation.
  cibuild  CI build.
  help     Display this text.
  instreq  Install required Python packages.
  publish  Publish generated documentation to web server.
  sphelp   Display Sphinx help text.
endef

.PHONY:	Makefile apidoc cibuild help instreq publish sphelp

help:
	$(info $(usage))
	@exit 0

sphelp:
	$(SPHINX_BUILD) -M help $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)

apidoc:
	sphinx-apidoc --force --output-dir $(SPHINX_SOURCE) ../letsdns
	rm $(SPHINX_SOURCE)/modules.rst
	$(SED_IE) 's/:(undoc-members:)/:no-\1/g' $(SPHINX_SOURCE)/*.rst

cibuild:	instreq apidoc html

instreq:
	pip install -r ../requirements.txt

publish:
	rsync $(RSYNC_OPTS) $(SPHINX_DEST)/html/ seichter@ra:/var/www/letsdns

%:	Makefile
	$(SPHINX_BUILD) -M $@ $(SPHINX_SOURCE) $(SPHINX_DEST) $(SPHINX_OPTS)
