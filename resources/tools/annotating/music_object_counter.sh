#!/bin/bash
# Music Object Counter (MOC) - Count music objects in JSON annotation files
# for optical music recognition (OMR) applications in a simple way.
# All JSON-files in folder will be examined.
#
# Copyright 2020 Florian Mysliwietz.
#
# There is NO warranty.  Redistribution of this software is
# covered by the Lesser GNU General Public License.
# =========================================================

version="0.1.0"
keywords=("clef" "key" "time" "primitive-component")

function versionCommand() {
    cat <<VERSION

Music Object Counter (MOC) version ${version}
Copyright 2020 Florian Mysliwietz.

There is NO warranty.  Redistribution of this software is
covered by the Lesser GNU General Public License.

VERSION
}

find_occurrences() {
    json_files=(./*.json)
    total_count=0
    for ((i = 0; i < ${#json_files[@]}; i++)); do
        echo "Search in ${json_files[$i]}"

        part_count=0
        for key in "${keywords[@]}"; do
            occurrences=$(grep -c "\"$key\":" "${json_files[$i]}")
            part_count=$((part_count + occurrences))
            printf "%-5s %s\n" "$occurrences" "$key"
        done

        total_count=$((total_count + part_count))

        printf "%-5s %s\n\n" "$part_count" "sum of music objects"
    done

    echo "Found overall $total_count music objects"
}

function main() {
    versionCommand
    find_occurrences
}

main "$@"
