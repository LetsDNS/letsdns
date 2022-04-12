Installation
============

Recommended: Python package
---------------------------

LetsDNS can be installed using the `Python Package Index`_. System-wide installation of Python packages usually requires
*root* privileges.

.. literalinclude:: _static/pip-install

.. _Python Package Index: https://pypi.org/project/letsdns/

Alternative: Virtual environment
--------------------------------

You can use LetsDNS in an isolated virtual environment, even as a non-*root* user. I provide an install script to create
such an environment from scratch. The following commands show how to invoke the script in a BASH compatible shell.

.. literalinclude:: _static/venv-install

Before launching LetsDNS for the first time, you need to create a `configuration`_ file.

.. _configuration: config.html
