# vim:ts=4:sw=4:noet

SED_INPLACE	?= /opt/local/bin/gsed -i''
VENV		= $(shell realpath .venv)
VERSION		?= $(shell echo "1.2.0.dev$$(date -u +'%j%H%M' | sed -e 's/^0//')")

define usage

Available make targets are:

  clean   Cleanup build artifacts.
  dist    Python distribution build.
  help    Display this text.
  push    Git push to all configured remotes.
  pypiup  Upload to PyPI.
  setver  Set application version.
endef

.PHONY:	clean dist help prep push pypiup setver

help:
	$(info $(usage))
	@exit 0

prep:
	@which pip | grep -q '^$(VENV)/bin/pip' || (echo 'Please execute:\n\n  source $(VENV)/bin/activate\n'; exit 1)

clean:
	rm -fr dist/*

dist:
	python -m build

push:
	@for r in $(shell git remote); do git push $$r; done

pypiup:	prep
	twine upload dist/*

setver:
	$(SED_INPLACE) -E -e "s/(^VERSION =).*/\1 '$(VERSION)'/" letsdns/__init__.py
	$(SED_INPLACE) -E -e "s/(^version =).*/\1 $(VERSION)/" setup.cfg
