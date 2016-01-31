#!/bin/bash

if [ "$#" -lt 1 ]; then
    echo "Act3 Work branch should be specified in docker run command."
	exit -1
fi

#trap "echo TRAPed signal" HUP INT QUIT KILL TERM
trap HUP INT QUIT KILL TERM

echo "cloning Act3"
git clone https://github.com/grnydawn/Act3.git

echo "cloning Act3"
# start service in background here
echo "starting shell"
/bin/bash

# stop service and clean up here
echo "stopping shell"

echo "exited $0"
