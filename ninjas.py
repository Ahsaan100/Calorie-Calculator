import requests
body = { 'text_1': 'My name is Ahsan', 'text_2': 'Ahsan is my name' }
api_url = 'https://api.api-ninjas.com/v1/textsimilarity'
response = requests.post(api_url, headers={'X-Api-Key':"dXqBwN7OX/SwZnocoYIrfw==J4rCrRIICM3i3nc6" }, json=body)
if response.status_code == requests.codes.ok:
    print(response.text)
else:
    print("Error:", response.status_code, response.text)
