casa6-docker/install
====================

This project provides two tools:

**casa6-docker**

    Create `Docker`_ images which contain a fully working data analysis and code development environment with modern modular `casa6`_ and other common Python packages (e.g. `astropy <https://www.astropy.org>`_, `Jupyter <https://www.jupyter.org/>`_, etc.), suitable for `Docker`_ or `Apptainer`_-based deployment.

**casa6-install**

    A Python-based command-line tool to help install `casa6` (monolithic or modular) on macOS or Linux, with options to manipulate abi/platform tags to force cross-installing release wheels on not officially supported Python versions and platforms. The container image building process of **casa6-docker** requires **casa6-install**.

=================   ====================================== 
**Documentation**   https://r-xue.github.io/casa6-docker  
**Repo**            https://github.com/r-xue/casa6-docker
**PyPI**            https://pypi.org/project/casa6-install
**Docker Hub**      https://hub.docker.com/r/rxastro/casa6 
=================   ======================================

Free open-source software: BSD license


.. note::

    - The Docker Hub image can be directly used with `Docker`_ (in macOS/Linux/Windows, commercial cloud services) or `Apptainer`_ (formally, Singularity, mainly for HPC).

.. _Docker: https://www.docker.com
.. _apptainer: https://apptainer.org/
.. _casa6: https://ui.adsabs.harvard.edu/abs/2020ASPC..527..271R/abstract