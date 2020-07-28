###################################################################################################
#
#   see documentation at http://r-xue.github.io/casa6-docker
#
#   + local build & login with Bash & check casatools version
#
#       $ # docker system prune --all 
#       # # export DOCKER_BUILDKIT=1
#       $ docker build -t casa6:latest --squash -f Dockerfile .
#       $ docker build -t casa6:base --squash -f Dockerfile.base .
#
#       $ docker image inspect casa6:base --format='{{.Size}}'
#       $ docker run -it casa6:base bash
#  
#   + pull Dockhub images & login rxastro/casa6:base with bash
#
#       $ docker pull rxastro/casa6:base # only for update    
#       $ docker run -it rxastro/casa6:base bash
#
###################################################################################################

FROM ubuntu:focal
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

RUN pip3 install --upgrade pip && \
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

####################################################################
# note: the content above this line is identical to Dockerfile.base
# Bonus (for development)
####################################################################

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
RUN echo -e "\
import os \n\
c.IPKernelApp.pylab = 'inline' \n\
c.NotebookApp.notebook_dir = '.' \n\
c.NotebookApp.ip = '0.0.0.0' \n\
c.NotebookApp.allow_remote_access = False \n\
c.NotebookApp.open_browser = False \n\
c.NotebookApp.port = int(os.environ.get('PORT', 8888)) \n\
c.NotebookApp.allow_root = True \n\
" >> ./.jupyter/jupyter_notebook_config.py
RUN pip3 install ipython numpy scipy \
        jupyterlab wurlitzer line_profiler memory_profiler \
        astropy bottleneck spectral-cube radio-beam \
        emcee corner && \
    rm -rf ./.cache/pip /tmp/* /var/tmp/*
RUN mkdir ./.casa && echo "telemetry_enabled = False" > ./.casa/config.py       
RUN pip3 install casadata casatasks casashell casaplotms casaviewer casatelemetry \
        --extra-index-url https://casa-pip.nrao.edu:443/repository/pypi-group/simple && \
    rm -rf ./.cache/pip /tmp/* /var/tmp/*
RUN pip3 list 

# more clean up

RUN rm -rf \
        ./.cache/pip \
        /var/lib/apt/lists/* \
        /tmp/* /var/tmp/*