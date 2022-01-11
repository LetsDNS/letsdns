# vim:ts=8:sw=8:noet

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINX_BUILD	?= PYTHONPATH=.. sphinx-build
SPHINX_OPTS	?=
SOURCE_DIR	= _source
BUILD_DIR	= _build

.PHONY:	apidoc help Makefile

help:
	$(SPHINX_BUILD) -M help "$(SOURCE_DIR)" "$(BUILD_DIR)" $(SPHINX_OPTS)

apidoc:
	sphinx-apidoc -f -o "$(SOURCE_DIR)" ../letsdns

%:	Makefile
	$(SPHINX_BUILD) -M $@ "$(SOURCE_DIR)" "$(BUILD_DIR)" $(SPHINX_OPTS)
