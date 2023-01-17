import requests
# just test api for rei reply 

url = "https://api.deepai.org/api/text-generator"
API-KEI = 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'

response = requests.post(
    url,
    data = {'text': 'tetx'},
    headers={'api-key': API-KEI}
)
print(response.json())
