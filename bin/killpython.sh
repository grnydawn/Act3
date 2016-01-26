#!/bin/bash

for f in `ps -e | grep python | cut -d ' ' -f 1`; do kill -9 $f; done
