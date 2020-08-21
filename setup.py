#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pip>20.0', 'wheel>=0.35.1']
setup_requirements = []
test_requirements = []

setup(
    author="Rui Xue",
    author_email='rx.astro@gmail.com',
    python_requires='>=3.7',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="",
    entry_points={
        'console_scripts': [
            'casa6_install = casa6_install.casa6_install:main'
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type="text/x-rst",
    include_package_data=False,
    keywords=['casa6', 'Docker', 'Singularity'],
    name='casa6-install',
    setup_requires=setup_requirements,
    packages=find_packages(include=['casa6_install', 'casa6_install.*']),
    url='https://github.com/r-xue/casa6-docker',
    project_urls={'Bug Reports': 'https://github.com/r-xue/casa-docker/issues',
                  'Source': 'https://github.com/r-xue/casa-docker'},
    version='1.1.4',
    zip_safe=False,
)
