#!/bin/bash

opts=("${*:2:$#}")

docker start -ai $opts $1
