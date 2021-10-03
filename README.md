# iPad-automate
Automated wiping, refresh and enrollment of iPad's managed via Cisco Meraki API / SolarWinds Help Desk API.

# How does the Zero-Touch Setup and Enrollment using Meraki Work
Note:  *We assume each iPad is Apple DEP enrolled into Meraki and supervised by a single Configurator 2 setup. Furthermore, **activation lock is enabled***.

1.  A pre-enrolled (Apple DEP), supervised device is running with a current Meraki profile loaded.

2.  Send **Remove Activation Lock and Erase** via Meraki Website or *preferred*, use the Python Meraki API to perform the same action.  The third option would be to run `cfguitl erase`.

3.  Device should be erased remotely within ~0 to ~30 seconds.

4.  If the device is Supervised we can run `cgutil install-profile wifi-autoconfig.mobileconfig` via the **Supervising Configurator 2** device.  This profile will cause the device to immediately connect to an available access point after it has been erased and search for a MDM (in our case Meraki).  This part is very important as it is completely hands-free and automated.  Without this step the user will need to manually connect to a Wifi network, provide credentials and allow the Meraki MDM enrollment.  They will also need to skip any setup assistant prompts.

5.  To ensure the user resetting iPads doesn't have to touch / configure any prompts ensure that the proper Profile configuration (inside Meraki->Systems Manager->Settings) is applied (this profile is create using the **Supervising Configurator 2** device).  Note:  **Make sure the profile is set to not display any setup assistant prompts.**

5.  Lastly, automatic renaming is done by monitoring the device state (for something like installed apps) until the device appears to be totally setup.  The device serial number is then queried passed to the SolarWinds Helpdesk API Endpoint.  The API responds with the appropriate Asset # and the device is then subsequently renamed this (`cfgutil rename <asset#>`).  If there are any system updates they are initiated and installed as well.  
---
**Configure Caching**:
On the **Supervising Configurator 2** device ensure that `System Preferences->Sharing->Caching` has been enabled.  This allows any iOS update to be cached and sent over USB to other connected iPads.  This drastically speeds up the update process.  When the device is fully updated it is unpaired from Configurator and the reset complete.  Disconnect the device and connect another. 
