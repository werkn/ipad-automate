###################################################################
# _          _           _           _                      _     #
#| |        | |         | |         | |                    (_)    # 
#| |__   ___| |_ __   __| | ___  ___| | ________ __ _ _ __  _     #
#| '_ \ / _ \ | '_ \ / _` |/ _ \/ __| |/ /______/ _` | '_ \| |    #
#| | | |  __/ | |_) | (_| |  __/\__ \   <      | (_| | |_) | |    #
#|_| |_|\___|_| .__/ \__,_|\___||___/_|\_\      \__,_| .__/|_|    #
#            | |                                    | |           #
#            |_|                                    |_|           #
###################################################################
# @author Ryan Radford <mailto:ryan@werkncode.net>                #
# helpdesk-api-python is used to support iPad remote management   #
###################################################################

import urllib.request
import json
import sys

HELPDESK_BASE_URL="your-solar-winds-helpdesk-endpoint-here"
HELPDESK_KEY_PATH = "/Users/configurator2/Desktop/keys/helpdesk.key"

# Gets the decrypted helpdesk API key from file (NOTE:  You
# must decrypt the key prior to use and maintain this key outside
# of any version control).  I highly recommend installing a kron/scheduled task
# to ensure the key is encrypted/decrypted at each logon and logoff.
def getAPIKeyFromFile(path):
    apiKey = open(path,'r').read().strip() #remove whitespace and read entire file (exp a single line)
    return apiKey

def getNotesForAsset(apiKey, assetNumber):
    "get the notes for an asset from the serial number"
    result = getAssetDetailsAsJSON(apiKey, assetNumber)
    result = result[0]["notes"]
    return result

# Return the asset details for provided assetNumber
def getAssetDetailsAsJSON(apiKey, assetNumber):
    "get asset details for assetNumber"
    getUrl = '{0}/ra/Assets?assetNumber={1}&apiKey={2}'.format(
        str(HELPDESK_BASE_URL), str(assetNumber), str(apiKey))
    result = doJSONRequest(getUrl)
    return result

# Query helpdesk for an asset with the desired key-value pair
def getAssetWithValue(apiKey, key, value, select, printToConsole):
    "Query helpdesk for an asset with the desired key-value pair"
    getUrl = '{0}/ra/Assets?qualifier=({1}%3D%27{2}%27)&apiKey={3}'.format(
        str(HELPDESK_BASE_URL), str(key), str(value), str(apiKey))
    result = doJSONRequest(getUrl)
    if printToConsole:
        print(result)
    result = result[0][select]
    return result

# Get serial number for provided assetNumber
def getSerialNumber(apiKey, assetNumber):
    "get serial number for assetNumber"
    result = getAssetDetailsAsJSON(apiKey, assetNumber)
    result = result[0]["serialNumber"]
    return result

def getAssetNumber(apiKey, serialNumber):
    "get the asset number from serial number"
    getUrl = '{0}/ra/Assets?qualifier=(serialNumber%3D%27{1}%27)&apiKey={2}'.format(
        str(HELPDESK_BASE_URL), str(serialNumber), str(apiKey))
    result = doJSONRequest(getUrl)
    result = result[0]["assetNumber"]
    return result

# Perform a web request and load response, returning JSON object
def doJSONRequest(url):
    "perform a web request and load response, returning JSON object"
    request = urllib.request.Request(url)

    #parsing response
    response = urllib.request.urlopen(request).read()
    data = json.loads(response.decode('utf-8'))
    return data

# Load api key on startup
apiKey = getAPIKeyFromFile(HELPDESK_KEY_PATH)

# Handle requests
if sys.argv[1] == "serialNumber":
    print(getAssetWithValue(apiKey, sys.argv[1], sys.argv[2], sys.argv[3], False))
elif sys.argv[1] == "assetNumber":
    print (getAssetDetailsAsJSON(apiKey, sys.argv[2])[0][sys.argv[3]])
