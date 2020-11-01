doks
----

Usage
=====

.. code-block:: bash

       doks [-h] [--auto] [--command] [--verbose] [--window WINDOW]
            [source] [target]

Description
===========

Write a .rst document for a single Python file

Positional arguments
====================

``source``
  .py file to create documentation for

``target``
  .rst file to write to. None means stdout

Optional arguments
==================

``-h``, ``--help``
  Show this help message and exit

``--auto``, ``-a``
  Automatically guess which files to read and write

``--command``, ``-c``
  Use command line help from executing source instead

``--verbose``, ``-v``
  Print more stuff

``--window WINDOW``, ``-w WINDOW``
  How many lines around an RST error to print (0 means
  "print everything")
