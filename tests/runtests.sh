#!/bin/bash

export PYTHONPATH=..
python3 -m unittest discover "$@"
