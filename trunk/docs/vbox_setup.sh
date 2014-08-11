#!/bin/bash
# vim:sw=2 ts=2 sts=2 expandtab:

# This is an example script, how to set up a virtual guest using
# VirtualBox. This configuration was tested with Solaris 10U9.

# This script only sets up the instance, it doesn't start the instance.

# Initially, a Solaris installation ISO is mounted. After installation,
# run the script with the "eject" argument, which will remove the CD
# from the machine, allowing to boot from the hard disk.

# Rough usage guideline:
#
# 1. Edit the script to set correct paths.
# 2. Run the script with the "setup" argument.
#    ./vbox_setup.sh setup
# 3. Start the instance:
#    VBoxHeadless --startvm Screencast --vnc --vncport 5902
# 4. Connect to the instance using a VNC client. Install Solaris.
# 5. Stop the instance.
# 6. Run the script with the "eject" argument to remove the installation
#    DVD.
#    ./vbox-setup.sh eject
# 7. Start the vm again using VBoxHeadless, and use it. Connect first
#    via VNC, then make it available via the network.
#
# If you want to destroy your VM, run this script with the "teardown"
# argument. Note that it will destroy the whole vm, including all its
# state and data.

set -x
set -u
set -e

readonly DISK_DIR="/var/somewhere"
readonly VM_NAME="examplevm"
readonly VNC_PORT=5902

readonly CD="/path/to/sol-10-u9-ga-x86-dvd.iso"
readonly DISK_IN_MB=50000
readonly MEMORY_IN_MB=1024
readonly OSTYPE="OpenSolaris_64"

readonly DISK_NAME="${VM_NAME}"
readonly VDI="${DISK_DIR}/${VM_NAME}/${DISK_NAME}.vdi"
# Examples: "Ubuntu_64", "OpenSolaris_64"

# The MAC address can be set up if you want to assign a specific IP address and
# a DNS name to your virtual host. dnsmasq can do that.
readonly MAC="080027000001"

# The serial console has to be enabled on the OS side
# http://docs.oracle.com/cd/E19150-01/820-1853-16/AppB.html

function vbox_setup {
VBoxManage createvm \
	--name "${VM_NAME}" \
	--basefolder "${DISK_DIR}" \
	--ostype "${OSTYPE}" \
	--register
VBoxManage modifyvm "${VM_NAME}" \
	--memory "${MEMORY_IN_MB}" \
	--acpi on \
	--boot1 dvd \
	--nic1 bridged \
	--bridgeadapter1 eth0 \
	--macaddress1 "${MAC}" \
	--audio null \
	--usb off \
	--nictype1 Am79C970A \
	--uart1 0x3F8 4 \
	--uartmode1 server /tmp/${VM_NAME}console
VBoxManage createhd \
	--filename "${VDI}" \
	--size "${DISK_IN_MB}"
VBoxManage storagectl "${VM_NAME}" \
	--name "IDE Controller" --add ide
VBoxManage storagectl "${VM_NAME}" \
	--name "SATA Controller" --add sata
vbox_attach_disk
vbox_insert_cd
}

function vbox_insert_cd {
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "IDE Controller" \
	--type dvddrive --device 0 --port 0 \
	--medium "${CD}"
}

function vbox_teardown {
VBoxManage unregistervm "${VM_NAME}" --delete
}

function vbox_eject {
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "IDE Controller" \
	--type dvddrive --device 0 --port 0 \
	--medium none
}

function vbox_detach_disk {
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "SATA Controller" \
	--type hdd --device 0 --port 0 \
	--medium "none"
}
function vbox_attach_disk {
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "SATA Controller" \
	--type hdd --device 0 --port 0 \
	--medium "${VDI}"
}

case "$1" in
  teardown) vbox_teardown ;;
  eject) vbox_eject ;;
  insert) vbox_insert_cd ;;
  setup) vbox_setup ;;
  fix-disk) vbox_fix_disk ;;
  run)
    VBoxHeadless --startvm ${VM_NAME} --vnc --vncport ${VNC_PORT}
    ;;
  *) echo >&2 Operation not supported. ;;
esac
