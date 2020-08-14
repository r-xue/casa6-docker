
Local Build
===========

You will need the GitHub repository for local image builds.

First, get the Docker files:

.. code-block:: console

    $ git clone https://github.com/r-xue/casa6-docker
    $ cd casa6-docker/

Then start to build local images

.. code-block:: console

    $ docker build -t casa6:latest --squash -f Dockerfile .
    $ docker build -t casa6:base --squash -f Dockerfile.base .

    $ docker image inspect casa6:lates --format='{{.Size}}'
    $ docker image inspect casa6:base --format='{{.Size}}'
    $ docker history casa6:latest    

Now you can log in the container instance from the freshly-built image:

.. code-block:: console

    $ docker run -it casa6:latest bash

Within the container, you can try something like this to verify the installation of casatools:

.. code-block:: python

    root@1313297097c3:~# python
    Python 3.8.2 (default, Jul 16 2020, 14:00:26) 
    [GCC 9.3.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import casatools
    >>> print('casatools ver:',casatools.version_string())
    casatools ver: 6.2.0.3    


.. _casatools: https://casa-pip.nrao.edu/#browse/browse:pypi-group:casatools