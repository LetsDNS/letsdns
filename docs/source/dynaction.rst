Dynamic actions
===============

LetsDNS functionality can be extended with the help of dynamically loaded action classes. This allows users to execute
actions which are not part of the official package, e.g. to update domain name servers with some proprietary mechanism,
accessing databases, and so forth.

Dynamic action classes need to be derived from the *letsdns.action.Action* abstract base class, and be available via
Python's *sys.path* or PYTHONPATH.

As an example, consider the following file/directory structure:

.. literalinclude:: _static/dynaction-tree

Assume further that the Python file action.py contains the following:

.. literalinclude:: _static/dynaction-py

You can reference this dynamic action using

    action = dynamic:sample.action.MyCustomAction

in your `configuration`_ files.

.. _configuration: config.html
