CASA6 Installation
==================

As of June 2020, the CASA6 core component `casatools`_ package is only available as Py36 `wheel <https://packaging.python.org/discussions/wheel-vs-egg>`_ for macOS/Linux.
If Python 3.6 is your default interpreter, you can just install it using Pip-3.6

.. code-block:: console

    $ pip-3.6 install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casatools

If you prefer Python >=3.7, we provide a workaround on the installation of `casatools`_ along with other casa6 modules, with sp provided by uvrx.
I should stress that this is used as a temperaible solution before the official support of the latest MacOS/Python from NRAO.
The procedure is demostrated under Macports-Python 3.8 (set as below), though this note should work on other Python distributions (e.g. Anaconda).

.. code-block:: console

    $ sudo port select --set python python38
    $ sudo port select --set ipython ipython38
    $ sudo port select --set pip pip38

.. _casatools: https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatools

How to install
---------------

+ Download the Py3.6 MacOS package, run this command (`pip download`_) in your terminal:

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


+ Then use the CLI tool (see :code:`$ casatools_repack --help`) provided by ``ism3d`` to modify the wheel package (here the file name is casatools-6.1.0.107-cp36-cp36m-macosx_10_15_x86_64.whl)

.. code-block:: console

    $ casatools_repack casatools-${casatools_version}-cp36-cp36m-macosx_${os_version}_x86_64.whl cp38


+ Install the rest CASA6 modules along with casatools.

.. code-block:: console

    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casadata
    $ pip install --user --upgrade \
        casatools-${casatools_version}-cp38-cp38-macosx_${os_version}_x86_64.whl
    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casatasks casashell casaplotms casaviewer   

The other CASA6 components (``casatasks``,``casashell``,``casaviewer``,``casaplotms``,``casampi``,`` casatelemetry``) are not platform specific and the installation can be done using the standard method.


Verify the Installation
-----------------------

.. ipython::

    In [1]: import casatasks, casatools
    
    In [2]: print('casatools ver:',casatools.version_string())
    
    In [3]: print('casatasks ver:',casatasks.version_string())

Tips & Tricks
--------------

+ Optionally, casampi can be installed,

.. code-block:: console

    $ export CXX=/opt/local/bin/g++
    $ export clang=/opt/local/bin/clang
    $ export gcc=/opt/local/bin/gcc
    $ sudo port install py38-mpi4py
    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casampi    

+ the locations of the CASA viewer and plotms apps is a little bit obscure, but are likely found here (if `pip --user` is used)::

    ~/Library/Python/3.8/lib/python/site-packages/casaviewer/__bin__/casaviewer.app
    ~/Library/Python/3.8/lib/python/site-packages/casaplotms/__bin__/casaplotms.app

+ You may need to remove previous installation before upgrading different moduels due to their inter-depdency (see below)::

.. code-block:: console

    $ pip uninstall --yes casadata casatools casatasks casaviewer casashell

+ Dependency

Sometimes, the dependecy among the latest whl relase is mismatached, but one can manully fix them by manuall picked a working version of CASA components by speciali the cmodule version, e.g,:

.. code-block:: console

    $ whlversion='6.1.0.107'
    $ pip install --user 
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casatasks==${whlversion}


Reference
---------

1. `PEP 425 -- Compatibility Tags for Built Distributions`_
2. `PEP 3149 -- ABI version tagged .so files`_
3. `The "m" ABI flag of SOABI for pymalloc is no longer needed`_

.. _PEP 425 -- Compatibility Tags for Built Distributions: https://www.python.org/dev/peps/pep-0425
.. _PEP 3149 -- ABI version tagged .so files: https://www.python.org/dev/peps/pep-3149
.. _The "m" ABI flag of SOABI for pymalloc is no longer needed: https://bugs.python.org/issue36707


