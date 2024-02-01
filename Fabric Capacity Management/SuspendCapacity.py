#!/usr/bin/env python3

"""
This script retrieves a list of subscriptions from Azure and resumes the capacities in each resource group.
"""
import automationassets
from requests_oauth2client import OAuth2Client, BearerToken
import requests
#Additional import for Azure Automation
from automationassets import AutomationAssetNotFound

token_endpoint=automationassets.get_automation_variable("token_endpoint")
client_id=automationassets.get_automation_variable("client_id")
client_secret=automationassets.get_automation_variable("client_secret")

#For local testing
# token_endpoint= ''
# client_id= ''
# client_secret= ''

# Get token
client = OAuth2Client( token_endpoint = token_endpoint, auth = (client_id, client_secret) )
token = client.client_credentials(scope ="resource", resource = "https://management.azure.com/")

# Get list of subscriptions
subscription_url = "https://management.azure.com/subscriptions?api-version=2023-07-01"
headers = {'Authorization': f'Bearer {token}'}
subscriptions_response = requests.get(subscription_url, headers=headers)
subscriptions = subscriptions_response.json()

for subscription in subscriptions['value']:
    # Get resource groups in subscription
    resource_groups_url = f"https://management.azure.com/subscriptions/{subscription['subscriptionId']}/resourcegroups?api-version=2023-07-01"
    resource_groups_response = requests.get(resource_groups_url, headers=headers)
    resource_groups = resource_groups_response.json()
    
    for resource_group in resource_groups['value']:
        # Get capacities in resource group
        capacities_url = f"https://management.azure.com/subscriptions/{subscription['subscriptionId']}/resourceGroups/{resource_group['name']}/providers/Microsoft.Fabric/capacities?api-version=2022-07-01-preview"
        capacities_response = requests.get(capacities_url, headers=headers)
        capacities = capacities_response.json()

        if capacities['value']:
            for capacity in capacities['value']:
                capacity_url = f"https://management.azure.com{capacity['id']}/suspend?api-version=2022-07-01-preview"
                payload = {}
                headers = {
                      'Authorization': f'Bearer {token}'
                    }
                response = requests.post(capacity_url, headers=headers, data=payload)

                print(response.status_code)
