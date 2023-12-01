###################################################################################################
#
#   see documentation at http://r-xue.github.io/casa6-docker
#
#   + local build & login with Bash & check casatools version
#
#       $ # docker system prune --all 
#       # # export DOCKER_BUILDKIT=1
#       $ docker build --target base -t casa6:base -f Dockerfile .
#       $ docker build --target latest -t casa6:latest -f Dockerfile .
#
#       $ docker image inspect casa6:base --format='{{.Size}}'
#       $ docker run -it --platform linux/amd64 casa6:base bash
#  
#   + pull Dockhub images & login rxastro/casa6:base with bash
#
#       $ docker pull rxastro/casa6:base # only for update    
#       $ docker run -it --platform linux/amd64 rxastro/casa6:base bash
#
###################################################################################################

ARG os_image=ubuntu:focal

# the stage to build casa6:base image

FROM ${os_image} AS base_build

LABEL maintainer="rx.astro@gmail.com"

# use bash instead of default sh

SHELL ["/bin/bash", "-c"] 
ENV APP_HOME /root
WORKDIR ${APP_HOME}
ENV DEBIAN_FRONTEND noninteractive

# run apt-get

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install --no-install-recommends -y \
    python3-pip wget python-is-python3 \
    libtinfo5 libquadmath0 \
    && \
    apt-get autoremove -y && \ 
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# add alias / configs / scripts / latest pip
#   RUN echo "alias pip='pip3'" > ./.bash_aliases

# add latest pip although pip3 still points to ubuntu/pip3 

RUN pip3 install --upgrade pip packaging && \
    rm -rf ./.cache/pip

# install latested casatools from NRAO

# note: casatools technically requires:
#   + numpy
#   + casadata (which I skip with --no-deps to keep the rx.astro/casa6:base image slim)
COPY casa6_install/casa6_install.py ./Downloads/
RUN echo "install casa6... may take a while in the container " && \
    python3 ./Downloads/casa6_install.py --core --no-deps && pip3 install numpy && pip3 list && \
    rm -rf ./.cache/pip /tmp/* /var/tmp/*
# libgfortran3 is not included in Ubuntu20.04 but required for current casa6-py36 whl
# here we copy .so filed from Ubuntu18.04
#   reference: https://pkgs.org
RUN wget http://archive.ubuntu.com/ubuntu/pool/universe/g/gcc-6/libgfortran3_6.4.0-17ubuntu1_amd64.deb && \
    dpkg-deb -c libgfortran3_6.4.0-17ubuntu1_amd64.deb && \ 
    dpkg-deb -R libgfortran3_6.4.0-17ubuntu1_amd64.deb / && \
    rm -rf ./libgfortran3_6.4.0-17ubuntu1_amd64.deb /DEBIAN

# clean up

RUN rm -rf \
    ./.cache/pip \
    /var/lib/apt/lists/* \
    /tmp/* /var/tmp/*

# the stage to compact casa6:base image

FROM scratch AS base
# alternatively also use '-w root' with docker run
WORKDIR /root
COPY --from=base_build / /

# the stage to build casa6:latest image, reduce layers

FROM base_build AS latest_build

# more apt install

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get install --no-install-recommends -y \
    nano less wget git gcc python3-dev \
    # gfortran build-essential make \
    # cython3 \
    # libfftw3-dev numdiff python3-pybind11 \
    && \
    apt-get autoremove -y && \     
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# add more Python packages

RUN mkdir ./.jupyter

RUN printf "%s\n" \
    "import os" \
    "c.IPKernelApp.pylab = 'inline'" \
    "c.ServerApp.notebook_dir = '.'" \
    "c.ServerApp.ip = '*'" \
    "c.ServerApp.allow_origin = ''" \
    "c.ServerApp.allow_remote_access = False" \
    "c.ServerApp.open_browser = False" \
    "c.ServerApp.port = int(os.environ.get('PORT', 8888))" \
    "c.ServerApp.allow_root = True" \
    "c.LabApp.news_url = None" \
    "c.LabApp.check_for_updates_class = 'jupyterlab.NeverCheckForUpdate'" \
    > ./.jupyter/jupyter_lab_config.py
RUN pip3 install ipython numpy scipy \
    jupyterlab wurlitzer line_profiler memory_profiler \
    astropy bottleneck spectral-cube radio-beam \
    emcee corner dask && \
    rm -rf ./.cache/pip /tmp/* /var/tmp/*
RUN mkdir ./.casa && echo "telemetry_enabled = False" > ./.casa/config.py       
RUN pip3 install casadata casatasks casashell casaplotms casaviewer \
    --extra-index-url https://casa-pip.nrao.edu/repository/pypi-casa-release/simple && \
    rm -rf ./.cache/pip /tmp/* /var/tmp/*
RUN pip3 list 

# more clean up

RUN rm -rf \
    ./.cache/pip \
    /var/lib/apt/lists/* \
    /tmp/* /var/tmp/*

# the stage to compact casa6:latest image, reduce layers

FROM scratch AS latest
# alternatively also use '-w root' with docker run
WORKDIR /root 
COPY --from=latest_build / /
