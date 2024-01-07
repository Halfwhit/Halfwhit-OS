#!/usr/bin/env bash
#
#  ██╗  ██╗ █████╗ ██╗     ███████╗██╗    ██╗██╗  ██╗██╗████████╗        ██████╗ ███████╗
#  ██║  ██║██╔══██╗██║     ██╔════╝██║    ██║██║  ██║██║╚══██╔══╝       ██╔═══██╗██╔════╝
#  ███████║███████║██║     █████╗  ██║ █╗ ██║███████║██║   ██║          ██║   ██║███████╗
#  ██╔══██║██╔══██║██║     ██╔══╝  ██║███╗██║██╔══██║██║   ██║          ██║   ██║╚════██║
#  ██║  ██║██║  ██║███████╗██║     ╚███╔███╔╝██║  ██║██║   ██║          ╚██████╔╝███████║
#  ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝      ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝   ╚═╝           ╚═════╝ ╚══════╝
#
#  NAME: Halfwhit OS
#  DESC: An installation and deployment script for Halfwhit's desktop.
#  WARNING: Run this script at your own risk.
#  DEPENDENCIES: libnewt

# First, check if the script is being ran as a normal user
if [ "$(id -u)" = 0 ]; then
	echo "##################################################################"
	echo "This script MUST NOT be run as root user since it makes changes"
	echo "to the \$HOME directory of the \$USER executing this script."
	echo "The \$HOME directory of the root user is, of course, '/root'."
	echo "We don't want to mess around in there. So run this script as a"
	echo "normal user. You will be asked for a sudo password when necessary."
	echo "##################################################################"
	exit 1
fi

# Set up an error function
error() { \
	clear; printf "ERROR:\\n%s\\n" "$1" >&2; exit 1;
}

# Set up colours for the TUI
export NEWT_COLORS="
root=,blue
window=,black
shadow=,blue
border=blue,black
title=blue,black
textbox=blue,black
radiolist=black,black
label=black,blue
checkbox=black,blue
compactbutton=black,blue
button=black,red"

# Install the single dependancy if not already installed
echo "##################################################################"
echo "## Syncing the repos and installing 'whiptail' if not installed ##"
echo "##################################################################"
sudo pacman --noconfirm --needed -Syu libnewt || error "Error syncing the repos."

welcome() { \
    whiptail --title "Installing Halfwhit OS!" --msgbox "This is a script that will install Halfwhit OS (Halfwhit's operating system).  It's really just an installation script for my tiling window manager configurations and associated programs.  You will be asked to enter your sudo password at various points during this installation, so stay near the computer." 16 60
}

welcome || error "User choose to exit."

speedwarning() { \
    whiptail --title "Installing Halfwhit OS!" --yesno "WARNING! The ParallelDownloads option is not enabled in /etc/pacman.conf. This may result in slower installation speeds. Are you sure you want to continue?" 16 60 || error "User choose to exit."
}

distrowarning() { \
    whiptail --title "Installing Halfwhit OS!" --msgbox "WARNING! While this script works on all Arch based distros, this hasn't been tested. If anyone else ever tries to use this script and has problems, please raise an issue on the Github page." 16 60 || error "User choose to exit."
}

grep -qs "#ParallelDownloads" /etc/pacman.conf && speedwarning
grep -qs "ID=arch" /etc/os-release || distrowarning

lastchance() { \
    whiptail --title "Installing Halfwhit OS!" --msgbox "WARNING! The Halfwhit OS installation script is permanently in public beta testing. There are almost certainly errors in it; therefore, it is strongly recommended that you not install this on production machines. It is recommended that you try this out in either a virtual machine or on a test machine." 16 60

    whiptail --title "Are You Sure You Want To Do This?" --yesno "Shall we begin installing Halfwhit OS?" 8 60 || { clear; exit 1; }
}

lastchance || error "User choose to exit."

# Set up locales
grep "LC_CTYPE" /etc/locale.conf && echo "Checking the LC_CYPE variable in /etc/locale.conf. Variable is already set." || grep "LANG=" /etc/locale.conf | sed 's/LANG=/LC_CTYPE=/g' | sudo tee -a /etc/locale.conf
sudo locale-gen