Installation
============

Method 1: Isolated environment
------------------------------

LetsDNS is currently in a pre-release state, and you might want to use it in an isolated execution environment, i.e. a
Python virtual environment. I provide an install script which does just that, and the following commands show how to
invoke the script in a BASH compatible shell. Note that this method is feasible for a non-*root* user.

.. literalinclude:: _static/venv-install

Before launching LetsDNS for the first time, you need to create a `configuration`_ file.

.. _configuration: config.html

Method 2: Python package
------------------------

As an alternative, LetsDNS can be installed system-wide, using the official Python package available from `PyPI`_.
This might require *root* privileges.

.. literalinclude:: _static/pip-install

.. _PyPI: https://pypi.org/project/letsdns/
