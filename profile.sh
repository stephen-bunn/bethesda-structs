#!/usr/bin/env bash
python -m cProfile -o .profile.cprof ${1:-main.py} && pyprof2calltree -k -i .profile.cprof && rm -rf .profile.cprof
