# vim:ts=8:sw=8:noet

SPHINX_BUILD	?= env PYTHONPATH=.. sphinx-build
SPHINX_OPTS	?=
SOURCE_DIR	= source
OUTPUT_DIR	= build

.PHONY:	apidoc cibuild help Makefile requirements

help:
	$(SPHINX_BUILD) -M help $(SOURCE_DIR) $(OUTPUT_DIR) $(SPHINX_OPTS)

cibuild:	requirements apidoc html
	
requirements:
	pip install -r ../requirements.txt

apidoc:
	sphinx-apidoc --force --output-dir $(SOURCE_DIR) ../letsdns
	rm $(SOURCE_DIR)/modules.rst
	sed -i'' -E -e 's/:(undoc-members:)/:no-\1/g' $(SOURCE_DIR)/*.rst

%:	Makefile
	$(SPHINX_BUILD) -M $@ $(SOURCE_DIR) $(OUTPUT_DIR) $(SPHINX_OPTS)
