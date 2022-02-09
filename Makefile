# vim:ts=4:sw=4:noet

PYPI_REPO	?= testpypi
VERSION		?= $(shell echo "0.1.dev$$(date -u +'%j%H%M' | sed -e 's/^0//')")

SEDI		= sed -i'' -E -e
VENV		= $(shell realpath .venv)
VERSIONQ	= '$(VERSION)'

PKG	= scripts/package

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
	$(SEDI) "s/(^VERSION =).*/\1 $(VERSIONQ)/" letsdns/__init__.py
	$(SEDI) "s/(^version =).*/\1 $(VERSION)/" setup.cfg
