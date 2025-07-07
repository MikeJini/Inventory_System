import requests
import json

VALS = [
    {
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with adjustable DPI and 2.4GHz connectivity.",
        "sku": "WM-ERG-001",
        "category": "Computer Accessories",
        "price": 24.99,
        "quantity": 30,
        "threshold": 10
    },
    {
        "name": "Wireless KeyBoard",
        "description": "wireless KeyBoard",
        "sku": "WM-ERG-002",
        "category": "Computer Accessories",
        "price": 39.99,
        "quantity": 30,
        "threshold": 10
    },
    {
        "name": "Mouse Pad",
        "description": "Mouse Pad",
        "sku": "WM-ERG-003",
        "category": "Computer Accessories",
        "price": 9.99,
        "quantity": 30,
        "threshold": 10
    }
]

for item in VALS:
    requests.post('http://192.168.1.217:5000/api/products', json=item)

# --- GET Request Products ---

# Define the URL for the GET request
get_url = "http://192.168.1.217:5000/api/products"

print(f"Making a GET request to: {get_url}")
# Make the GET request
get_response = requests.get(get_url)

# Check if the request was successful (status code 200)
if get_response.status_code == 200:
    print("GET request successful!")
    # Print the JSON response content
    print("Response JSON:")
    print(json.dumps(get_response.json(), indent=2))
else:
    print(f"GET request failed with status code: {get_response.status_code}")

print("\n" + "="*30 + "\n")    