#!/bin/bash

for f in `ps -e | grep python | cut -d ' ' -f 2`; do kill -9 $f; done
