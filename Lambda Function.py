import json
import os
from botocore.vendored import requests


def lambda_handler(event, context):
	#This calls the Halo 5 Data API key from the AWS Lambda environment variable "apikey"
    apikey = os.environ["apikey"]
    #Get player's basic info
    appearance = requests.get("https://www.haloapi.com/profile/h5/profiles/cfh%20hateph34r/appearance",  headers={'Ocp-Apim-Subscription-Key': apikey})
    #Get player's arena record
    servicerecord = requests.get("https://www.haloapi.com/stats/h5/servicerecords/arena?players=cfh%20hateph34r",  headers={'Ocp-Apim-Subscription-Key': apikey})
    #Get player's commendation record
    commrecord = requests.get("https://www.haloapi.com/stats/h5/players/cfh%20hateph34r/commendations",  headers={'Ocp-Apim-Subscription-Key': apikey})
    #Get list of all commendation names
    comm = requests.get("https://www.haloapi.com/metadata/h5/metadata/commendations",  headers={'Ocp-Apim-Subscription-Key': apikey})
	#If all queries return successfully, create a dict with results from all queries
    if appearance.status_code == 200 and servicerecord.status_code == 200 and commrecord.status_code == 200 and comm.status_code == 200:
        data = {
            "appearance":appearance.json(),
            "servicerecord":servicerecord.json(),
            "commrecord":commrecord.json(),
            "comm":comm.json()
        }
		#Return success (200), with data as the body
        return {
            "statusCode": 200,
            "headers": {
            "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(data)
            
        }
    else:
		#Return failure(500) with error message as body
        return {
            "statusCode": 500,
            "headers": {
            "Access-Control-Allow-Origin": "*",
             },
            "body": "ERROR: Failed to retrieve data from Halo 5 servers. Please refresh the page to try again."
             }