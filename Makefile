# vim:ts=8:sw=8:noet

PKG = contrib/package

.PHONY:	clean dist docs push usage

usage:
	@echo >&2 "Usage: make {clean | dist | docs | push}"
	@exit 1

clean:
	$(PKG) clean || true

dist:
	$(PKG) dist

docs:
	$(PKG) docs

push:
	@for r in $(shell git remote); do git push $$r; done
