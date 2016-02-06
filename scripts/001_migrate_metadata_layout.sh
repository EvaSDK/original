#!/bin/bash

if [ $# -ne 1 ]; then
    cat <<EOF
Usage: $0 PATH

  Convert view count and comments from sequentially numbered layout to
  filename based layout.
EOF
    exit 2
fi

while IFS= read -r -d '' gallery
do
    while IFS= read -r -d '' log
    do
        target="$(echo "${log}" | sed 's/log_/img-/;s/.txt/.jpg.log/;')"
        echo mv "${log}" "${target}"
    done < <(find "${gallery}" -type f -name "log_*.txt" -print0)

    while IFS= read -r -d '' comments
    do
        if echo "${comments}" | grep -q ".jpg" ; then
            continue
        fi
        target="$(echo "${log}" | sed 's/\(.*\)\/\(.*\).txt/\1\/img-\2.jpg.txt/')"
        mv "${comments}" "${commentdir}"/"${target}"
    done < <(find "${gallery}" -type f -name "*.txt" -print0)

done < <(find "${1}" -type d -name "comments" -print0)
