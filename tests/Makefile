# vim:ts=8:sw=8:noet

COVERAGE_DIR		?= ../local/coverage
SKIP_ONLINE_TESTS	?= no
UNITTEST_CONF		?= ../local/devtest.conf

ENV_VARS		= env PYTHONPATH=.. SKIP_ONLINE_TESTS=$(SKIP_ONLINE_TESTS) UNITTEST_CONF=$(UNITTEST_CONF)

.PHONY:	coverage coverage-html run-tests

run-tests:
	$(ENV_VARS) python -m unittest discover -v

coverage:
	$(ENV_VARS) coverage run -m unittest discover
	coverage report

coverage-html:	coverage
	coverage html -d $(COVERAGE_DIR) --skip-empty --no-skip-covered
	open $(COVERAGE_DIR)/index.html
