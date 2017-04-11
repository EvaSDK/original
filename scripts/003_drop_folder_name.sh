#!/bin/bash

if [ $# -ne 1 ]; then
    cat <<EOF
Usage: $0 PATH

  Remove folder-name from info.txt as it is not useful and not required anymore.
EOF
    exit 2
fi

while IFS= read -r -d '' infofile
do
    sed -i '/folder-name.*/d' "${infofile}"
done < <(find "${1}" -type f -name "info.txt" -print0)
