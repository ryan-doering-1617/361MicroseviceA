import requests

# Request data
payload = {
    "num_questions": 5,
    "total_questions": 50,
    "previously_selected": [3, 8, 15]
}

# Send POST request
response = requests.post("http://localhost:5025/randomize", json=payload)

# Print the response
print(response.json())