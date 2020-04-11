PyTK - Python ToolKit
=====================

**PyTK** - Python ToolKit:
Python abstract graphical user-interface toolkit

This Python library intend to provide a sensible abstraction layer on top of
the most widely used GUI toolkits.
This is similar to `AnyGUI <https://wiki.python.org/moin/AnyGui>`_
except that we focus more on offering full and stable support for the standard
Python GUI toolkit.

For the moment, however, only a few tricks for common ``tkinter`` implementation
patterns are in place.

The widget semantic follows, when possible, HTML conventions.

There are plans to includes support for Text-based UIs (via ``asciimatics``).

Installation
------------
The recommended way of installing the software is through
`PyPI <https://pypi.python.org/pypi/pytk>`_:

.. code:: shell

    $ pip install pytk

Alternatively, you can clone the source repository from
`GitHub <https://github.com/norok2/pytk>`_:

.. code:: shell

    $ mkdir pytk
    $ cd pytk
    $ git clone git@github.com:norok2/pytk.git
    $ python setup.py install

(some steps may require additional permissions depending on your configuration)

The software does not have additional dependencies beyond Python and its
standard library.

It was tested with Python 2.7 and 3.5.
Other version were not tested.
