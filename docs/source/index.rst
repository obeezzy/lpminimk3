.. lpminimk3 documentation master file, created by
   sphinx-quickstart on Mon Apr 10 19:21:44 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

=======================
lpminimk3 documentation
=======================

.. image:: https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml/badge.svg
    :target: https://github.com/obeezzy/lpminimk3/actions/workflows/main.yml
    :alt: GitHub workflow
.. image:: https://github.com/obeezzy/lpminimk3/actions/workflows/deploy.yml/badge.svg?branch=v0.5.1
    :target: https://github.com/obeezzy/lpminimk3/actions/workflows/deploy.yml
    :alt: Github releases

.. image:: images/mk3.jpg
    :align: center
    :width: 200px

lpminimk3 is the free and unofficial Python API for the `Novation Launchpad Mini MK3 <https://novationmusic.com/en/launch/launchpad-mini>`_.

Goals
=====

- Intuitive, object-oriented design
- Convenient for use in script and shell
- Access to all (or most) of the Launchpad Mini MK3 MIDI features

Features
========

- Full LED control
- Text rendering
- Bitmap rendering
- Movie rendering
- Console rendering
- Button press and release handling
- Control over a network via websockets
- Multiple launchpad control

Installation
============

To install the most stable version of this package, run:
  ``$ pip install lpminimk3``

To test the installation, connect your Launchpad to your computer and run:
  ``$ python -m lpminimk3.examples.hello``

.. toctree::
   :maxdepth: 1
   :caption: Reference

   reference/lpminimk3
