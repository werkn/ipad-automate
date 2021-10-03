#!/bin/bash
#@author: Ryan Radford (ryan@werkncode.net)

#############
# setup     #
#############

echo "~~~Starting iPad-setup~~~"
echo "Accept pairing on device, then press return"
read 

# gather required device info
serialNumber=`cfgutil get serialNumber`
startName=`cfgutil get name`
assetTag="not found"

#############
# functions #
#############

# get proper asset tag from remote (helpdesk)
# getAssetTag( serialNumber ) 
function getAssetTag {
	echo `python3 helpdesk-api-python.py serialNumber "${serialNumber}" assetNumber`  
}

# renameDevice ( assetTag )
function renameDevice {
	echo "Getting Asset Tag from Helpdesk (this may take ~30 - 40 seconds)..."
	assetTag=`getAssetTag`
	echo "Attempting to rename ${startName} to ${assetTag}..."
	cfgutil rename "${assetTag}"
	echo "Renamed device."
}

# update the to latest iOS, requires the device running 
#cfgutil to have internet connection
function doUpdate {
	echo "Attempting iOS Update..."
	cfgutil update 
}

function unpairDevice {
	echo "Unpairing device..."
	cfgutil unpair 
	echo "Device Unpaired..."
}

function getHelpDeskNotes {
	echo "Helpdesk Notes: "
	echo `python3 helpdesk-api-python.py assetNumber "${assetTag}" notes`  
}

#############
#   start   #
#############

#getAssetTag
renameDevice 
doUpdate
unpairDevice
getHelpDeskNotes
#append device asset tag to audit log (for automated review later)
echo ${assetTag} >> ~/Desktop/audit.log
