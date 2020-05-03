#!/bin/bash
FILE_FILTER=$2
TESTS_FILTER="$3"

python -m pip install -r ../jobs_launcher/install/requirements.txt

python ../jobs_launcher/executeTests.py --test_filter $TESTS_FILTER --file_filter $FILE_FILTER --tests_root ../jobs --work_root ../Work/Results --work_dir TAN