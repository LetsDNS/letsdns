# vim:ts=8:sw=8:noet

PKG	= scripts/package

.PHONY:	clean dist push usage

usage:
	@echo >&2 "Usage: make {clean | dist | push}"
	@exit 1

clean:
	$(PKG) clean || true

dist:
	$(PKG) dist

push:
	@for r in $(shell git remote); do git push $$r; done
