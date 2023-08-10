#!/bin/bash

# Enter virtualenv
source env/bin/activate

PYTHONPATH=src:. pytest

# Exit virtualenv
deactivate

