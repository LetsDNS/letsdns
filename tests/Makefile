# vim:ts=4:sw=4:noet

ENABLE_ONLINE_TESTS	?= no
UNITTEST_CONF		?= ../local/devtest.conf

COVDIR	= ../local/coverage
UTENV 	= env PYTHONPATH=.. ENABLE_ONLINE_TESTS=$(ENABLE_ONLINE_TESTS) UNITTEST_CONF=$(UNITTEST_CONF)

.PHONY:	coverage coverage-html run-tests

run-tests:
	$(UTENV) python -m unittest discover -v

coverage:
	$(UTENV) coverage run --include='../letsdns/*' -m unittest discover
	coverage report --rcfile=.coveragerc

coverage-html:	coverage
	coverage html -d $(COVDIR) --title='LetsDNS test coverage' --skip-empty --no-skip-covered
	open $(COVDIR)/index.html
