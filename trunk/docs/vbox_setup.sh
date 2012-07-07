#!/bin/bash

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

DISK_DIR="/var/somewhere"
VM_NAME="Example VM"
VDI="${DISK_DIR}/${VM_NAME}/example.vdi"
CD="/path/to/for/example/sol-10-u9-ga-x86-dvd.iso"
DISK_SIZE=20000
RAM_MB=1024
OSTYPE="OpenSolaris_64"
# So that you can set up your DNS and DHCP to give a specific IP address
# and assign a name based on a MAC address. dnsmasq can do that.
MAC="08:00:27:00:00:01"

function setup {
VBoxManage createvm \
	--name "${VM_NAME}" \
	--basefolder "${DISK_DIR}" \
	--ostype "${OSTYPE}" \
	--register
VBoxManage modifyvm "${VM_NAME}" \
	--memory "${RAM_MB}" \
	--acpi on \
	--boot1 dvd \
	--nic1 bridged \
	--bridgeadapter1 eth0 \
	--macaddress "${MAC}" \
	--audio null \
	--usb off
VBoxManage createhd \
	--filename "${VDI}" \
	--size "${DISK_SIZE}"
VBoxManage storagectl "${VM_NAME}" \
	--name "IDE Controller" --add ide
VBoxManage storagectl "${VM_NAME}" \
	--name "SATA Controller" --add sata
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "SATA Controller" \
	--type hdd --device 0 --port 0 \
	--medium "${VDI}"
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "IDE Controller" \
	--type dvddrive --device 0 --port 0 \
	--medium "${CD}"
}

function teardown {
VBoxManage unregistervm "${VM_NAME}"
rm -rf "${DISK_DIR}/${VM_NAME}"
}

if [[ "$1" == teardown ]]
then
	teardown
elif [[ "$1" == eject ]]
then
VBoxManage storageattach "${VM_NAME}" \
	--storagectl "IDE Controller" \
	--type dvddrive --device 0 --port 0 \
	--medium none
elif [[ "$1" == setup ]]
then
	setup
fi
