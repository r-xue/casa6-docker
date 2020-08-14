
Brief
=====

The GitHub `repository <https://github.com/r-xue/casa6-docker>`_ contains a `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile>`_, which automatically builds two ``casa6-docker`` images hosted at the `Docker Hub <https://hub.docker.com/r/rxastro/casa6/tags>`_.
These images contain a base Linux environment (upon `Ubuntu 20.04 <https://releases.ubuntu.com/20.04/>`_) with `casa6 <https://casa.nrao.edu/casa_obtaining.shtml>`_ and other Python packages (`astropy <https://www.astropy.org/>`_, `Jupyter <https://jupyter.org>`_, etc.) already installed. 

    https://registry.hub.docker.com/r/rxastro/casa6

The difference between these two images (tags) is described as below:
    
- `rxastro/casa6:latest <https://hub.docker.com/r/rxastro/casa6/tags>`_

    designed to provide a "developmental" environment with many Python packages installed

        - python3.8, pip, ipython, scipy, numpy, matplotlib 
        - `casatools <https://pypi.org/project/casashell/>`_, `casatasks <https://pypi.org/project/casatasks/>`_, `casashell <https://pypi.org/project/casashell/>`_, `casaplotms <https://pypi.org/project/casaplotms/>`_, `casaviewer <https://pypi.org/project/casaviewer/>`_, etc.
        - astropy
        - jupyterlab, etc.

    some general-purpose Linux utilities are included

        - nano, git, wget

    the container footprint is reasonable (~1GB) and efforts have been made to reduce its size (minimize and stash layers)


- `rxastro/casa6:base <https://hub.docker.com/r/rxastro/casa6/tags>`_

    designed to be used as a "slim" base image with a smaller footprint, built with `Dockerfile.base <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile.base>`_, only including

        - python3.8, numpy, casatools
    
    The standard ``casatools`` module can be used as an alternative to `python-casacore <https://github.com/casacore/python-casacore>`_ for MeasurementSet I/O.
    One of its dependency ``casadata`` is intentionally excluded in this build to reduce the image size.
