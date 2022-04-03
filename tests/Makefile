# vim:ts=8:sw=8:noet

COVERAGE_DIR		?= ../local/coverage
ENABLE_ONLINE_TESTS	?= no
UNITTEST_CONF		?= ../local/devtest.conf

ENV_VARS		= env PYTHONPATH=.. ENABLE_ONLINE_TESTS=$(ENABLE_ONLINE_TESTS) UNITTEST_CONF=$(UNITTEST_CONF)

.PHONY:	coverage coverage-html run-tests

run-tests:
	$(ENV_VARS) python -m unittest discover -v

coverage:
	$(ENV_VARS) coverage run --include='../letsdns/*' -m unittest discover
	coverage report --rcfile=.coveragerc

coverage-html:	coverage
	coverage html -d $(COVERAGE_DIR) --title='LetsDNS test coverage' --skip-empty --no-skip-covered
	open $(COVERAGE_DIR)/index.html
