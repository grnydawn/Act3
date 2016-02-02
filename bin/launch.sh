#!/bin/bash

# a folder that contains this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# list of service names in Act3
svcs=("name" "sdb" "kdb" "udb" "comp" "xform" "web")
args=("$@") 
cmds=()
pids=()

# check if a service is in the list
containsElement () {
   local e
   for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
   return 1
}

# put services in order
for svc in "${svcs[@]}"; do
    containsElement "${svc}" "${args[@]}"
    if [ "$?" == "0" ]; then
        cmds+=("${svc}")
    fi
done

# launch each services
for cmd in "${cmds[@]}"; do
    if [ -f "${DIR}/../${cmd}/main.py" ]; then
        python3 ${DIR}/../${cmd}/main.py &
		if [ "$?" == "0" ]; then
			pids+=("$!")
		fi
    fi
done

# save process ids for termination
echo ${pids[@]} > $DIR/.pids
##wait ${pids[@]}
