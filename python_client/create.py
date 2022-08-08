import requests

endpoint = "http://127.0.0.1:8000/api/products/"
data = {
    "title" : "This is perform_create title",
    "price" : 54.21
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())
