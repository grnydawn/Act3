#!/bin/bash

opts=("${*:2:$#}")

docker create --name act3dev -h act3dev -it -p 8080:8080 -p 9090:9090 $opts grnydawn/act3_dev:v2 $1

if [ "$?" == 0 ]; then
    "act3dev Docker container is successfully created."
else
    "act3dev Docker container is NOT correctly created."
fi
