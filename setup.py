#!/usr/bin/env python

# encoding: utf-8


"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ['wheel']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

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
            'casa6_install = casa6install.casa6install:main'
        ],
    },
    install_requires=requirements,
    license="BSD license",
    long_description=readme,
    long_description_content_type="text/x-rst",
    include_package_data=True,
    keywords='casa6',
    name='casa6-install',
    url='https://github.com/r-xue/casa6-install',
    version='1.0',
    zip_safe=False
)