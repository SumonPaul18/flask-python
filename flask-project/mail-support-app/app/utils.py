import requests

def process_barracuda_request(domain, receiver_email, sender_email):
    url = "https://api.barracuda.com/v1/process"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    data = {
        "domain": domain,
        "receiver_email": receiver_email,
        "sender_email": sender_email
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()