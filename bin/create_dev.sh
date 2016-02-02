#!/bin/bash

name=act3dev
opts=("${*:2:$#}")

docker create --name $name -h $name -it -p 8080:8080 -p 9090:9090 $opts grnydawn/act3_dev:v2 $1

if [ $? -eq 0 ]; then
    echo "$name Docker container is successfully created."
else
    echo "$name Docker container is NOT correctly created."
fi
