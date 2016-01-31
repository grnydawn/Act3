#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "An Act3 Work branch should be specified in docker run command."
	exit -1
fi

#trap "echo TRAPed signal" HUP INT QUIT KILL TERM
trap HUP INT QUIT KILL TERM

cd /root

echo "cloning Act3"
git clone https://github.com/grnydawn/Act3.git

echo "checking-out a branch"
cd Act3
git fetch
git checkout $1

echo "starting a shell"
/bin/bash

echo "checking if there are changes"
new=`git status | grep "new file" | wc -l`
mod=`git status | grep "modified" | wc -l`
ren=`git status | grep "renamed" | wc -l`
#del=`git status | grep "deleted" | wc -l`
#changed=$((new + mod + ren + del))
changed=$((new + mod + ren))

if [ "$changed" -gt 0 ]; then
	me=`uname -n`
	now=`date`
	cd /root/Act3
	git add .
	git commit -m "Automated commit for $me at $now" 	
	if [ "$?" -ne 0 ]; then
		echo "git commit was failed. Please resolve the issue before leaving."
		/bin/bash
	fi
	git push origin $1
	if [ "$?" -ne 0 ]; then
		echo "git push was failed. Please resolve the issue before leaving."
		/bin/bash
	fi
fi

echo "exited $0"
