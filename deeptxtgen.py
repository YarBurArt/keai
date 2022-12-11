import requests

r = requests.post(
    "https://api.deepai.org/api/text-generator",
    data={
        'text': 'tetx',
    },
    headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
)
print(r.json())