#!/usr/bin/env python
# -*- coding: utf-8 -*-

# python 2.7
import requests, json

token_url = "https://api.districtm.ca/oauth/token"

api_url = "https://api.districtm.ca/looker/queries/json"

client_id = '' # Get from Account Manager
client_secret = '' # Get from Account Manager

auth_data = {'grant_type': 'client_credentials'}

access_token_response = requests.post(token_url, data=auth_data, allow_redirects=False,
                                      auth=(client_id, client_secret))

tokens = json.loads(access_token_response.text)

print("Bearer: " + tokens['access_token'])

api_request_payload = '{"model":"api","view":"boost3_metrics_api","fields":["boost3_metrics_api.day_date","boost3_metrics_api.domain_name","boost3_metrics_api.zone_name","boost3_metrics_api.product","boost3_metrics_api.media_type","boost3_metrics_api.placement_id","boost3_metrics_api.country","boost3_metrics_api.adsize","boost3_metrics_api.tagname","boost3_metrics_api.ad_requests","boost3_metrics_api.net_earnings_usd","boost3_metrics_api.net_ecpm_usd"],"filters":{"boost3_metrics_api.day_date":"2019/06/01 to 2019/06/03"}}'

api_call_headers = {'Authorization': 'Bearer ' + tokens['access_token']}
api_call_headers['Content-Type'] = 'application/json'
api_call_response = requests.post(api_url, headers=api_call_headers, data=api_request_payload)

print api_call_response.text
