#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

for pid in `cat $DIR/.pids`; do
	kill -9 $pid
done
rm -f $DIR/.pids
