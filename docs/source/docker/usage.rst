
Usage
=====

.. note::

    You don't need the repository content to use the `Docker Hub <https://hub.docker.com/r/rxastro/casa6/tags>`_ images. 

Launch with an interactive shell
--------------------------------

To launch the container with an interactive shell on a host with `Docker Desktop <https://docs.docker.com/docker-for-mac/install/>`_ running, just type:

.. code-block:: console

    $ docker run -it --platform linux/amd64 -v ~/Workspace:/root/WorkDir rxastro/casa6:latest bash

This will download the image ``rxastro/casa6:latest``, start a container instance, and login as ``root`` (bravely...). It will also try to mount the host directory ``~/Workspace`` (assuming it exists) to ``/root/WorkDir`` of your container.
After this, you can perform code development and data analysis in ``/root/WorkDir`` of your container (now pointing to ``~/Workspace`` on the host), with access of tools/environment (e.g. **casa6**, **astropy**, etc.) residing in the image.

In case you would like to manually update local-cached images for whatever reasons, you probably want to run this before launching the container again:

.. code-block:: console

    $ docker pull rxastro/casa6:latest


Use with Jupyter
----------------

A Jupyter server has been built in the Docker image ``rxastro/casa6:latest`` (see the `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile>`_ content for its customization).
This creates a useful feature of ``rx.astro/casa6:latest``: you can connect your host web browser to the Jupyter server running its container instance.
This gives you a portable development environment semi-isolated from your host OS that offers all Jupyter-based features (e.g. `Widgets <https://ipywidgets.readthedocs.io>`_) along with many Python packages: **casatools**, **casatasks**, **astropy**, **numpy**, **matplotlib**, and more.

To log in a ``rxastro/casa6:latest`` container and start the Jupyter session,

.. code-block:: console

    user@host      $ docker run --platform linux/amd64 -v ~/Workspace:/root/WorkDir --env PORT=8890 -it -p 8890:8890 rxastro/casa6:latest bash
    root@container $ jupyter-lab # start a Jupyter session

Then you can move back to the host, open a web browser, and connect it to the Jupyter server running on the guest OS:

.. code-block:: console

    user@host      $ firefox --new-window ${address:8890-with-token}

*work-in-progress*: If you download the `example data and notebooks <https://github.com/r-xue/casa6-docker/blob/master/notebooks/>`_ and put them in ``~/Workspace`` on the host, you should be able to re-run them in your firefox window as shown in the example pages: `ism3d.uvhelper <https://r-xue.github.io/casa6-docker/html/notebooks/demo_api_uvhelper.html>`_, `ism3d.arts <https://r-xue.github.io/casa6-docker/html/notebooks/demo_api_arts.html>`_, and `ism3d.arts.lens <https://r-xue.github.io/casa6-docker/html/notebooks/demo_api_lens.html>`_

Use with Apptainer (formally, Singularity)
--------------------

Docker and OCI containers are supported by `Apptainer <https://apptainer.org/docs/user/main/docker_and_oci.html>`_ for HPC-based deployment:

.. code-block:: console

    $ apptainer pull docker://rxastro/casa6:latest
    $ file casa6_latest.sif
    $ apptainer inspect casa6_latest.sif
    $ apptainer exec casa6_latest.sif /bin/bash

.. note::
    
    - There are significant design `differences <https://apptainer.org/docs/user/main/docker_and_oci.html>`_ between Docker and Apptainer, and a detailed demonstration is beyond the scope of this documentation.

    - Apptainer offers `various <https://apptainer.org/docs/user/main/bind_paths_and_mounts.html>`_ options to bind paths/mounts.

As a Docker base image
--------------------------

You can start from the `Dockerfile <https://github.com/r-xue/casa6-docker/blob/master/Dockerfile>`_ of ``rxastro/casa6:latest``, edit it (e.g., add more packages or your pipeline/workflow), and build a local image to your specification (see `the local build instruction <http://r-xue.github.io/casa6-docker/html/docker/build.html>`_).

You can also directly use the online Docker Hub image as the base image for your custom build, which may save some time. 
Just put ``FROM: rxastro/casa6:latest`` in your Dockerfile.