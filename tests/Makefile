# vim:ts=8:sw=8:noet

UNITTEST_CONF ?= ../local/devtest.conf

.PHONY:	run-tests

run-tests:
	env PYTHONPATH=.. UNITTEST_CONF=$(UNITTEST_CONF) python -m unittest discover -v
