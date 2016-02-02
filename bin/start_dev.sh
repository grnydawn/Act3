#!/bin/bash

if [ "$#" -lt 1 ]; then
    container=act3dev
else
    container=$1
    opts=("${*:2:$#}")
fi

docker start -ai $opts $1
