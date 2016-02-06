#!/bin/bash

if [ $# -ne 1 ]; then
    cat <<EOF
Usage: $0 PATH

  Convert filenames to be lexicographically ordered by default.
EOF
    exit 2
fi

normalize() {
    # $1 path to normalize
    # $2 extension or target file
    orig="$(realpath -m -s "${1}")"
    dir="$(dirname "${orig}")"
    increment=$(basename "${1}" | sed -n 's/.*img-\([^.]*\).*/\1/; s/0*\([^0]\)/\1/;p')
    target="$(printf "img-%03d%s" ${increment} ${2})"
    [ "${orig}" = "${dir}"/"${target}" ] && return
    mv "${orig}" "${dir}"/"${target}"
}

while IFS= read -r -d '' gallery
do

    while IFS= read -r -d '' log
    do
    	normalize "${log}" ".jpg.log"
    done < <(find "${gallery}" -type f -name "*.jpg.log" -print0)

    while IFS= read -r -d '' comments
    do
    	normalize "${comments}" ".jpg.txt"
    done < <(find "${gallery}" -type f -name "*.jpg.txt" -print0)

    while IFS= read -r -d '' pic
    do
    	normalize "${pic}" ".jpg"
    done < <(find "${gallery}"/.. \( -type f -o -type l \) -name "*.jpg" -print0)

done < <(find "${1}" -type d -name "comments" -print0)


