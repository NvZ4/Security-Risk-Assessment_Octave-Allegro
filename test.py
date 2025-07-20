import requests

response = requests.get("http://127.0.0.1:3000/asset", params={"project_id": 13})
print(response.json())

