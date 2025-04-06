# vim: ts=4 sw=4 noet

SEDI	?= sed -i "" -E
VENV	= $(shell realpath .venv)
ver		?= $(shell echo "1.2.1.dev$$(date -u +'%j%H%M' | sed -e 's/^0//')")

define usage

Available make targets:

  clean   Cleanup build artifacts.
  dist    Python distribution build.
  help    Display this text.
  push    Git push to all configured remotes.
  pypiup  Upload to PyPI.
  schk    Shell script check.
  setver  Set application version.

Example usage:

  make setver ver=$(shell echo "1.2.2.dev$$(date +'%j' | sed -E 's/^0+//')")
endef

.PHONY:	clean dist help prep push pypiup schk setver

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
	@for _r in $(shell git remote); do git push $$_r; done; unset _r

pypiup:	prep
	twine upload dist/*

schk:
	shellcheck -x scripts/*

setver:
	$(SEDI) "s/(^VERSION =).*/\1 '$(ver)'/" letsdns/__init__.py
	$(SEDI) "s/(^version =).*/\1 $(ver)/" setup.cfg
