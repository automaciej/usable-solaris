#!/bin/bash
#
# $Id$
#
# Helps set up VirtualBox virtual machiine.
#
# Use -h to see help.

set -u
set -e

source "vbox-config.sh"

function image_create {
  $vb createvdi \
    -filename "${hd}" \
    -size "${disk_size}"
}

function mount_dvd {
  $vb modifyvm "${vmname}" \
   -dvd "${dvd}"
}

function umount_dvd {
  $vb modifyvm "${vmname}" -dvd none
}

set_up() {
  $vb createvm \
    -name "${vmname}" \
    -register

  $vb modifyvm "${vmname}" \
    -ostype Solaris \
    -memory 512m \
    -acpi off \
    -hda "${hd}" \
    -nic1 hostif \
    -hostifdev1 vbox0 \
    -nictype1 82540EM \
    -cableconnected1 on \
    -nicspeed1 10000 \
    -vrdp on \
    -vrdpport "${vrdpport}" \
    -boot1 dvd
  mount_dvd
}

tear_down() {
  $vb modifyvm "${vmname}" -hda none ||  true
  umount_dvd
  $vb unregistervm "${vmname}" ||  true
  rm -rf "~/.VirtualBox/Machines/${vmname}"
}

function usage {
  cat <<EOF
Usage:
$0 [ create-disk-image | setup | start | teardown | mount_dvd | umount_dvd ]
EOF
}

function main {
  local action=${1:-}
  case "${action}" in
    setup)
      set_up
      ;;
    teardown)
      tear_down
      ;;
    start)
      $vbh --startvm ${vmname} --vrdp on --vrdpport ${vrdpport}
      echo "rdesktop $(hostname --fqdn):${vrdpport}"
      ;;
    create-disk-image)
      image_create
      ;;
    mount_dvd)
      mount_dvd
      ;;
    umount_dvd)
      umount_dvd
      ;;
    *)
      echo >&2 "Huh?"
      usage
      exit 1
      ;;
  esac
}

main "$@"

# vim:bg=dark:
