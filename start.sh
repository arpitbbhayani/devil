#!/bin/bash

source venv/bin/activate

#
# Execution Phase
#

python run.py $@

#
# Breakdown Phase
#

deactivate
