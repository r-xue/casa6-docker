casa6-docker/install
====================

This project provides two tools:

**casa6-docker**

    create `Docker`_ images which contain a fully working data analysis and code development environment with modern modular `casa6`_ and other common Python packages (e.g. `astropy <https://www.astropy.org>`_, `Jupyter <https://www.jupyter.org/>`_, etc.), suitable for `Singularity`_-based HPC deployment.

**casa6-install**

    a Python-based command-line tool to help install `casa6`_ under Py37/38 on macOS or Linux (only for experimental use before the official NRAO support). The building process of **casa6-docker** requires **casa6-install**.

=================   ====================================== 
**Documentation**   https://r-xue.github.io/casa6-docker  
**Repo**            https://github.com/r-xue/casa6-docker
**PyPI**            https://pypi.org/project/casa6-install
**Docker Hub**      https://hub.docker.com/r/rxastro/casa6 
=================   ======================================

Free open-source software: BSD license


.. note::

    - The Docker Hub image can be directly used with `Docker`_ (in macOS/Linux/Windows, commercial cloud services) or `Singularity`_ (mainly for HPC).

    - **casa6** is still in development and considered as experimental. Its ``casatools`` package can be used as an alternative to `casacore <https://github.com/casacore/python-casacore>`_ for `MeasurementSet <https://casa.nrao.edu/Memos/229.html>`_ manipulation. I haven't run into issues with ``tclean``, ``mstransform``, etc. and the lower-level `Toolkit <https://casa.nrao.edu/docs/CasaRef/CasaRef.html>`_.


.. _Docker: https://www.docker.com
.. _Singularity: https://sylabs.io
.. _casa6: https://ui.adsabs.harvard.edu/abs/2019arXiv191209439R/abstract