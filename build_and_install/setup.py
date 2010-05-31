#!/usr/bin/env python

from setuptools import setup

setup(
    name='pySPARROW',
    version='0.4',
    description='An ojbect-oriented Python package for calculating water quality loadings using the SPARROW model',
    author='Jon Goodall and John Fay',
    author_email='goodall@engr.sc.edu',
    url='http://code.google.com/p/pysparrow/',
    packages=['pySPARROW'],
    install_requires=['pySPARROW'],
    long_description="""
    pySPARROW is an API for performing water quality modeling.  It is based on the USGS SPARROW model
        and implements the prediction portion of SPARROW in an Object-Orieted, Open Source Programming
        language. It can be used to create water quality analysis scripts that address specific places 
        and questions.""",
    classifiers=[
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Intended Audience :: Developers",
    "Development Status :: Beta"]
    )
