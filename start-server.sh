#!/bin/bash

# Enter virtualenv
source env/bin/activate

PYTHONPATH=src python3 app.py

# Exit virtualenv
deactivate

