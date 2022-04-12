Operation
=========

To run LetsDNS in a BASH compatible shell, you can use the commands below. LetsDNS does **not** require *root*
privileges. Read access to the configuration files and certificates suffices. The system account of your ACME client is
usually a good choice.

.. literalinclude:: _static/bash-run

One or more configuration files are required to run LetsDNS. If your shell supports wildcard expansion, you can use this
to launch LetsDNS with a variable number of arguments:

.. literalinclude:: _static/bash-wildcard

This BASH example invokes LetsDNS with all matching files. It allows you to place additional configuration files into
the */var/lib/letsdns* directory if the number of domains changes. These files might even be dynamically generated
during certificate retrieval.
