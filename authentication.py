# Required package requests: `pip install requests`

import json
import base64
import requests
from datetime import datetime
import os
# Using of Client Credentials authorization flow.
# Insert your client credentials received in welcome email.

client_id = "fortnera05@gmail.com_api_client_1665024978"
client_secret = "6cefac5564044d33bfb671ec81ca552e"

today = input("Input todays date in the format: yyyy/mm/dd: ")
symbol = input("Input ticker symbol: ")
expiry_date = input("Input the expiration date in the fomat: yyyy/mm/dd: ")
strike = input("Input the strike price: ")
type = input("Input 'C' for call and 'P' for put: ")

identity_url = "https://id.livevol.com/connect/token"
api_url = "https://api.livevol.com/v1/delayed/allaccess/market/option-and-underlying-quotes?root=SPY&option_type="+ type +"&date=" + today + "&min_expiry=" + expiry_date + "&max_expiry=" + expiry_date + "&min_strike=" + strike + "&max_strike=" + strike + "&symbol=" + symbol

authorization_token  = base64.b64encode((client_id + ':' + client_secret).encode())
headers = {"Authorization": "Basic " + authorization_token.decode('ascii')}
payload = {"grant_type": "client_credentials"}

# Requesting access token
token_data = requests.post(identity_url, data=payload, headers=headers)

if token_data.status_code == 200:
    access_token = token_data.json()['access_token']
    if len(access_token) > 0:
        print("Authenticated successfully")
        
		# Requesting data from API
        result = requests.get(api_url, headers={"Authorization": "Bearer " + access_token})
        result = result.json()
        options_data = result['options'][0]
        S = result['underlying_close']
        K = options_data['strike']
        r = options_data['rho']
        v = options_data['iv']
        today = datetime.strptime(today, '%Y-%m-%d')
        expiry = datetime.strptime(options_data['expiry'], '%Y-%m-%d')
        t = (expiry - today).days
        argv = './a.out ' + str(S) + ' ' + str(K) + ' ' + str(r) + ' ' + str(v) + ' ' + str(t)
        os.system(argv)
        print("Real price is " + str(options_data['option_close']))
else:
    print("Authentication failed")