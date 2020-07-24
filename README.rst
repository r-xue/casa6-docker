CASA6-install
==================

As of July 2020, the CASA6 core component `casatools`_ is only available as Py36 `wheels <https://packaging.python.org/discussions/wheel-vs-egg>`_ for macOS/Linux.
If Python 3.6 is your default interpreter, you may just use pip-3.6 with `this requirements file <./requirements_casa6pip36.txt>`_ for installation.

.. code-block:: console

    $  pip install --user --upgrade -r requirement_casa6pip36.txt

However, if your prefer using Python >=3.7 for your workflow/development, the above procedure won't work.

The Python-based command-line program from **casa6-install** provide a temporary workaround on this installation issue, before the `official support <https://pypi.org/project/casatools/>`_ of the latest Python and OS from `NRAO <https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage>`_.
It will install `casatools`_ along with other casa6 modules in one step (tested on macOS10.15 and Ubuntu20.04), let you have a working copy of casa6 modules under Python >=3.7.

The program is not affliated with NRAO in any way, and only for code developmental purpose, i.a. writing a new Python program using casa6 modules.

.. _casatools: https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatools

Install
-------

To install the CLI tool, just use one of these two options:

.. code-block:: console

    pip install --user git+https://github.com/r-xue/casa6-install.git # from GitHub
    pip install --user casa6-install                                  # from PyPI (likely

You may also just download the python module file `casa6install/casa6install.py` and use it directly, without installation.

Usage
-----

After installation, just type::

.. code-block:: console

    $ casa6_install

A full summary of **casa6_install** commands is available via

.. code-block:: console

    $ casa6_install --help

To use the module directly, typek

.. code-block:: console

    $ python casa6install.py

Verify the Installation
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    In [1]: import casatasks, casatools
    
    In [2]: print('casatools ver:',casatools.version_string())
    
    In [3]: print('casatasks ver:',casatasks.version_string())


Background
----------

Essentiall, the program does the following procedures:

First, it download the latest Py36 whl to a working directory using `pip download`_. The requiavelent console command is,

.. _pip download: https://pip.pypa.io/en/stable/reference/pip_download/

.. code-block:: console

    $ pip download --python-version 36 --abi cp36m --no-deps \
        --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple \
        casatools

If you want a specific version, try to run these line instead:

.. code-block:: console

    $ casatools_version='6.1.0.107'
    $ os_version='10_15'
    $ curl -O https://casa-pip.nrao.edu/repository/pypi-group/packages/casatools/${whlversion}/casatools-${whlversion}-cp36-cp36m-macosx_${os_version}_x86_64.whl

or equivalently

.. code-block:: console

    $ pip download --python-version 36 --abi cp36m --no-deps  \
        --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple \
        casatools==${casatools_version}

Then it will perform some nesscary modiftion to the downloaded whl package, and re-package it with the correct abi matching to your system.

Finally it will spawn a subprocess and install the modified whl pacakeg, as well as all requested modueld indepdent from python version, as we The other CASA6 components (``casatasks``,``casashell``,``casaviewer``,``casaplotms``,``casampi``,`` casatelemetry``) are not platform specific and the installatio
The eqauivelent console command will be something like:

.. code-block:: console

    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casadata
    $ pip install --user --upgrade \
        casatools-6.1.0.107-cp36-cp36m-macosx_10_15_x86_64.whl ## assume you're working on macOS10.15
    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casatasks casashell casaplotms casaviewer  

Notes
-----


+ the locations of the CASA **viewer** and **plotms** apps is a little bit obscure and site in the site-packages directory, something like (if `pip --user` is used)::

    ~/Library/Python/3.8/lib/python/site-packages/casaviewer/__bin__/casaviewer.app
    ~/Library/Python/3.8/lib/python/site-packages/casaplotms/__bin__/casaplotms.app

+ You may need to remove previous installation before upgrading different moduels due to their inter-depdency:

.. code-block:: console

    $ pip uninstall --yes casadata casatools casatasks casaviewer casashell

Reference
---------

1. `PEP 425 -- Compatibility Tags for Built Distributions`_
2. `PEP 3149 -- ABI version tagged .so files`_
3. `The "m" ABI flag of SOABI for pymalloc is no longer needed`_
4. `Requirements File Format`_
5. `Using pip from your program`_

.. _PEP 425 -- Compatibility Tags for Built Distributions: https://www.python.org/dev/peps/pep-0425
.. _PEP 3149 -- ABI version tagged .so files: https://www.python.org/dev/peps/pep-3149
.. _The "m" ABI flag of SOABI for pymalloc is no longer needed: https://bugs.python.org/issue36707
.. _Requirements File Format: https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format
.. _Using pip from your program: https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
