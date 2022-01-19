# vim:ts=8:sw=8:noet

UNITTEST_CONF		?= ../local/devtest.conf
SKIP_ONLINE_TESTS	?= no

.PHONY:	coverage run-tests

run-tests:
	env PYTHONPATH=.. SKIP_ONLINE_TESTS=$(SKIP_ONLINE_TESTS) UNITTEST_CONF=$(UNITTEST_CONF) python -m unittest discover -v

coverage:
	env PYTHONPATH=.. SKIP_ONLINE_TESTS=$(SKIP_ONLINE_TESTS) UNITTEST_CONF=$(UNITTEST_CONF) coverage run -m unittest discover
	coverage report
