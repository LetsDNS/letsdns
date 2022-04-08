# vim:ts=4:sw=4:noet

PYPI_REPO	?= testpypi
SED_INPLACE	?= /opt/local/bin/gsed -i''
VERSION		?= $(shell echo "1.0.dev$$(date -u +'%j%H%M' | sed -e 's/^0//')")
VENV		= $(shell realpath .venv)
VERSIONQ	= '$(VERSION)'

.PHONY:	clean dist help prep push pypi-upload setver

help:
	@echo >&2 "Usage: make {clean | dist | push | setver}"
	@exit 1

prep:
	@which pip | grep -q '^$(VENV)/bin/pip' || (echo 'Please execute:\n\n  source $(VENV)/bin/activate\n'; exit 1)

clean:	prep
	rm -fr dist/*

dist:
	python -m build

push:
	@for r in $(shell git remote); do git push $$r; done

pypi-upload:	prep
	twine upload --sign --identity 6AE2A84723D56D985B340BC08E5FA4709F69E911 --repository $(PYPI_REPO) dist/*

setver:
	$(SED_INPLACE) -E -e "s/(^VERSION =).*/\1 $(VERSIONQ)/" letsdns/__init__.py
	$(SED_INPLACE) -E -e "s/(^version =).*/\1 $(VERSION)/" setup.cfg
