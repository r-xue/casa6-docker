Brief
=====

As of July 2020, the `casa6 <https://ui.adsabs.harvard.edu/abs/2019arXiv191209439R/abstract>`_ core component `casatools <https://open-bitbucket.nrao.edu/projects/CASA/repos/casa6/browse>`_ is only available as Py36 `wheels <https://packaging.python.org/discussions/wheel-vs-egg>`_ for `macOS/Linux <https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatools>`_.
If Python 3.6 is the default interpreter, you can just use `pip-3.6` with `this requirements file <https://github.com/r-xue/casa6-docker/blob/master/requirements_casa6pip36.txt>`_ for installation.

.. code-block:: console

    $  pip install --user --upgrade -r requirement_casa6pip36.txt

However, if you are using Python >=3.7 for workflow/development, the standard ``pip`` procedure won't work.

**casa6-install** provides a command-line program as a temporary workaround on the current installation issue, before the `official support <https://pypi.org/project/casatools/>`_ of the latest Python and OS from `NRAO <https://casa.nrao.edu/casadocs/casa-5.6.0/introduction/casa6-installation-and-usage>`_.
It can help install `casatools`_ along with other **casa6** modules in one step (tested on macOS10.15 and Ubuntu20.04), let you have a working copy of **casa6** modules with Python >=3.7.


Usage
=====

You have two options to use the **casa6-install**:

Option 1: Install as a Python Package and Run the CLI tool 
----------------------------------------------------------

Install the tool from PyPi or the GitHub repository, e.g., 

.. code-block:: console

    $ pip install --user casa6-install

With the "--user" option, you must add the user-level bin directory (e.g., ~/Library/Python/3.8/bin) to your `PATH` environment variable. After this, try:

.. code-block:: console

    $ casa6_install --user --upgrade

A full summary of the ``casa6_install`` command options is available:

.. code-block:: console

    $ casa6_install --help

Option 2: Use the Python Module Directly
----------------------------------------

You may download the python module file `casa6_install/casa6_install.py <casa6_install/casa6_install.py>`_ and use it directly:

.. code-block:: console

    $ python casa6_install.py


.. note::

    - The program is not affiliated with NRAO and the official CASA6 development. It only serves for code developmental purposes, e.g., building/testing your own Python program/pipeline using **casa6** modules. The tool modifies the official Py36 .whl file to make it "compatible" with Py37/38 (see *Background* below). It doesn't build a binary from scratch.

    - Although the *hacking* approach in **casa-install** will get working **casa6** modules on macOS>=10.14 with Python>=3.7, it doesn't guarantee that the installed package will work properly on Linux. This is due to various library dependency (e.g. lack of ``libgfortran3``) and many potential differences between the building platform and your local OS distribution. Specifically for Ubuntu20.04, please check out this `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile>`_ on how to work around the dependency issue (involving the manual installation of ``libtinfo5``, ``libquadmath0``, ``libgfortran3``). For this moment, I found no issue at least when using ``casatools`` and ``casatasks`` for development purposes.

    - You may need to remove previous installations before upgrading modules due to version inter-dependency:
    .. code-block:: console

        $ pip uninstall --yes casadata casatools casatasks casaviewer casashell

Smoke Test
==========

.. code-block:: python

    In [1]: import casatasks, casatools
    
    In [2]: print('casatools ver:',casatools.version_string())
    casatools ver: 6.2.0.3

    In [3]: print('casatasks ver:',casatasks.version_string())
    casatasks ver: 6.2.0.3


Background
==========

The program essentially performs the following procedures:

First, **casa6-install** downloads the latest Py36 .whl for Linux or macOS to a working directory (default to ``/tmp``) using ``pip download``. 
The equivalent command will be,

.. _pip download: https://pip.pypa.io/en/stable/reference/pip_download/

.. code-block:: console

    $ pip download --python-version 36 --abi cp36m --no-deps \
        --extra-index-url https://casa-pip.nrao.edu/repository/pypi-group/simple \
        casatools

Then it will unpack ``.whl``, perform necessary modifications to files inside, and repack them with the correct `ABI <https://www.python.org/dev/peps/pep-3149>`_ matching to your Python versions.

Finally, it will spawn a subprocess and install the modified ``.whl``, along with other **casa6** packages (i.e., ``casatasks``, ``casashell``, ``casaviewer``, ``casaplotms``, ``casampi``, ``casatelemetry``) which are not platform-specific.
The equivalent console command will be something like:

.. code-block:: console

    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casadata
    $ pip install --user --upgrade \
        casatools-6.1.0.107-cp36-cp36m-macosx_10_15_x86_64.whl ## assume you're working on macOS10.15
    $ pip install --user --upgrade \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple \
        casatasks casashell casaplotms casaviewer 

+ The locations of the **casaviewer** and **plotms** are a little bit obscure and will sit in the ``site-packages`` directory, e.g. (if ``pip --user``)::

    ~/Library/Python/3.8/lib/python/site-packages/casaviewer/__bin__/casaviewer.app
    ~/Library/Python/3.8/lib/python/site-packages/casaplotms/__bin__/casaplotms.app

+ You may need to remove previous installations before upgrading modules due to version inter-dependency,

.. code-block:: console

    $ pip uninstall --yes casadata casatools casatasks casaviewer casashell

