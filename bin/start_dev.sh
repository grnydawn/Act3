#!/bin/bash

opts=("${*:2:$#}")

docker run -it -P $opts grnydawn/act3_dev:v1 $1
