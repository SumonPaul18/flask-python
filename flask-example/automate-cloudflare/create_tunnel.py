import requests
import json

# Replace with your Cloudflare account details
API_TOKEN = 'your_cloudflare_api_token'
ACCOUNT_ID = 'your_cloudflare_account_id'
TUNNEL_NAME = 'your_tunnel_name'
TUNNEL_HOSTNAME = 'your_tunnel_hostname'

# Cloudflare API endpoint for creating a tunnel
url = f'https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/tunnels'

# Headers for the API request
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

# Data for creating the tunnel
data = {
    'name': TUNNEL_NAME,
    'config': {
        'ingress': [
            {
                'hostname': TUNNEL_HOSTNAME,
                'service': 'http://localhost:8080'  # Replace with your local service
            }
        ]
    }
}

# Make the API request to create the tunnel
response = requests.post(url, headers=headers, data=json.dumps(data))

# Check the response
if response.status_code == 200:
    print('Tunnel created successfully!')
    print(response.json())
else:
    print('Failed to create tunnel')
    print(response.status_code, response.text)
