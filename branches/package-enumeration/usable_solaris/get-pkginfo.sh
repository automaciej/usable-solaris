#!/bin/bash
#
# A temporary solution, defines functions for data retrieval.
# Setting up ssh keys and using keychain is convenient.

set -u

do_host() {
  local h="$1"
  echo -n "${h}... "
  if [[ ! -s "${h}.pkginfo" ]]; then
    echo -n "pkginfo... "
    ssh "$h" pkginfo -l > "$h.pkginfo"
    echo -n "done. "
  fi
  if [[ ! -s "${h}.showrev" ]]; then
    echo -n "showrev... "
    ssh "$h" showrev -p > "$h.showrev"
    echo -n "done. "
  fi
  echo
}

get_data_from_file() {
  local file_name="$1"
  for h in $(cat "${file_name}"); do
    do_host "${h}"
  done
}

main() {
  get_data_from_file "$1"
}

main "$@"
