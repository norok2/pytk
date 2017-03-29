PyTK - Python ToolKit
=====================

**PyTK** - **Py**thon **T**ool**K**it:
Python abstract graphical user-interface toolkit

This Python library intend to provide a sensible abstraction layer on top of
the most widely used GUI toolkits.
This is similar to `AnyGUI <https://wiki.python.org/moin/AnyGui>`_
except that we focus more on offering full and stable support for the standard
Python GUI toolkit.

The widget semantic follows HTML conventions.

There are plans to includes support for Text-based UIs (via ``asciimatics``).

Installation
------------
The recommended way of installing the software is through
`PyPI <https://pypi.python.org/pypi/pytk>`_:

.. code:: shell

    $ pip install autoui

Alternatively, you can clone the source repository from
`Bitbucket <https://bitbucket.org/norok2/pytk>`_:

.. code:: shell

    $ mkdir autoui
    $ cd autoui
    $ git clone git@bitbucket.org:norok2/autoui.git
    $ python setup.py install

(some steps may require additional permissions depending on your configuration)

The software does not have additional dependencies beyond Python and its
standard library.

It was tested with Python 2.7 and 3.5.
Other version were not tested.
