#!/bin/bash
#
# Run a single test file with coverage.
#
nosetests --with-coverage --cover-erase --nocapture $1
