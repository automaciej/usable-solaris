#!/bin/bash
#
# A temporary solution, defines functions for data retrieval.
# Setting up ssh keys and using keychain is convenient.

set -u

do_host() {
  local h="$1"
  if [[ ! -s "${h}.pkginfo" ]]; then
    echo -n "pkginfo ${h}... "
    ssh "$h" pkginfo -l > "$h.pkginfo"
    echo done
  fi
  if [[ ! -s "${h}.showrev" ]]; then
    echo -n "showrev ${h}... "
    ssh "$h" showrev -p > "$h.showrev"
    echo done
  fi
}

get_data_from_file() {
  local file_name="$1"
  for h in $(cat "${file_name}"); do
    do_host "${h}"
  done
}
