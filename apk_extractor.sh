#!/usr/bin/env bash

############################################################################
#																	   	   #
# Script to directly extract apk files from Android Device via ADB 		   #
#								   	   									   #	
# Example usage: 						   	  							   #
#	Show all packages installed:				   	   					   #
#		./apk_extractor					   	   							   #
#	Show all packages from google:					   					   #
#		./apk_extractor google					   						   #
#	Show all packages from google and export to custom directroy:	       #
#		./apk_extractor google /home/jnsm/Documents/Mobile/Apps	    	   #
#									   									   #
# (c) Jannik Schmied, 2022						   						   #
#									   									   #
############################################################################

usage () {
	echo -e "[i] Usage: $0 [<App Name>] [<Extraction Destination>]
	\t\n* App Name			 e.g. Threema (Default: all)
	\t\n* Extraction Destination	 e.g. /home/user/Documents (Default: /home/user/Downloads/apks)"
}

clean () {
	rm /tmp/packages.lst
}


if [ $# -gt 2 ] ; then
	usage
	exit 1 
fi

ADB_READY=`adb devices | wc -l`

if [ $ADB_READY -ne 3 ] ; then
	echo "[!] Error: ADB is not ready or multiple devices are connected. Please connect single device and try again."
	exit 1
fi

ADB_DEVICE=`adb devices | head -2 | tail -1 | awk '{print $1}'`
APP_NAME="*"
DESTINATION=/home/$(whoami)/Downloads/apks
DESTINATION_TYPE="default"

if [ $# -eq 1 ] ; then 
	APP_NAME=$1
fi

if [ $# -eq 2 ] ; then
	if [ -d $2 ] ; then
		DESTINATION=$2
	else
		mkdir $DESTINATION
	fi
	DESTINATION_TYPE="custom"
fi

echo "-------------------------------------------------------------------------"
echo -e "[i] Using ADB device:\t\t\t\t$ADB_DEVICE"
echo -e "[i] Using $DESTINATION_TYPE extraction destination:\t$DESTINATION"
echo -e "[i] Searching for packages matching app name:\t$APP_NAME"
echo -e "-------------------------------------------------------------------------\n"

# Searching full package name and write results to temporary file
adb shell pm list packages | grep -E "$APP_NAME" | awk -F 'package:' '{print $2}' > /tmp/packages.lst

if [[ "$(cat /tmp/packages.lst)" == "" ]] ; then
	echo "[!] Error: no matching packages found for app name '$APP_NAME'."
	exit 1
fi

declare -i ITER=1

echo -e "[*] Found $(cat /tmp/packages.lst | wc -l) results:\n"

# Print matching packages for selection
while IFS= read -r LINE ; do
	echo -e "[$ITER] $LINE"
	ITER=$ITER+1
done < <(cat /tmp/packages.lst)

# Getting selection from user
echo -e "\n[0] Exit\n"
read -p "[?] Please choose from [number]: " SELECTION

if [ $SELECTION -eq 0 ] ; then
	echo -e "[i] Exit. Bye!\n"
	exit 0
fi

# Handling possible selection errors
if [ $SELECTION -gt $ITER ] ; then
	echo -e "[!] Error: selection out of range. Using last result."
	SELECTION=$ITER
fi

if [ $SELECTION -lt 1 ] ; then 
	echo -e "[!] Error: selection out of range. Using first result."
	SELECTION=1
fi

# Extract matching packet name
PACKAGE_NAME=`cat /tmp/packages.lst | head -$SELECTION | tail -1 | awk '{print $1}'`

echo -e "\n[*] Extracting package $PACKAGE_NAME"

# Get full path of the app
PACKAGE_PATH=`adb shell pm path $PACKAGE_NAME | awk -F 'package:' '{print $2}'`

echo -e "[*] Full path is $PACKAGE_PATH\n"

# Extract app to desired local path (Downloads folder by default)
if adb pull $PACKAGE_PATH $DESTINATION ; then
	echo -e "\n[+] Success: extracted $APP_NAME ($PACKAGE_NAME) to $DESTINATION"
	EXIT_CODE=0
else
	echo -e "\n[!] Error: could not extract $PACKAGE_NAME."
	EXIT_CODE=1
fi

clean

echo
exit $EXIT_CODE
