#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

svcs=("name" "sdb" "kdb" "udb" "comp" "xform" "web")
args=("$@") 
cmds=()
pids=()

containsElement () {
   local e
   for e in "${@:2}"; do [[ "$e" == "$1" ]] && return 0; done
   return 1
}

for svc in "${svcs[@]}"; do
    containsElement "${svc}" "${args[@]}"
    if [ "$?" == "0" ]; then
        cmds+=("${svc}")
    fi
done

for cmd in "${cmds[@]}"; do
    if [ -f "${DIR}/../${cmd}/main.py" ]; then
        python3 ${DIR}/../${cmd}/main.py &
        pids+=("$!")
        sleep 3
    fi
done

#echo ${pids[@]}  
#wait ${pids[@]}
