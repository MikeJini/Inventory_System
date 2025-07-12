import requests
import json
import sys

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

api_port = sys.argv[1] # Take in as parameter from pipeline
get_url = fr"http://127.0.0.1:{api_port}/api/products"
test_id_delete = None

for item in VALS:
    response = requests.post(get_url, json=item)

    print(type(response.status_code))

    if response.status_code <= 200 and response.status_code >= 204:
        raise Exception(f"GET request failed with status code: {response.status_code}")

# --- GET Request Products ---

print(f"Making a GET request to: {get_url}")
# Make the GET request
get_response = requests.get(get_url)

# Check if the request was successful (status code 200)
if get_response.status_code >= 200 and get_response.status_code <= 204:
    print("GET request successful!")
    # Print the JSON response content
    print("Response JSON:")
    data = get_response.json()

    print(json.dumps(data, indent=2))

    test_id_delete = data[0]["id"]
else:
    raise Exception(f"GET request failed with status code: {get_response.status_code}")

print("\n" + "="*30 + "\n")    

# --- Delete Request Products ---

print(f"Making a GET request to: {get_url}/{test_id_delete}")
# Make the Delete request
get_response = requests.delete(f"{get_url}/{test_id_delete}")

# Check if the request was successful (status code 200)
if get_response.status_code >= 200 and get_response.status_code <= 204:
    print("GET request successful!")
    # Print the JSON response content
    print("Response JSON:")
    print(json.dumps(get_response.json(), indent=2))
else:
    raise Exception(f"DELETE request failed with status code: {get_response.status_code}")

print("\n" + "="*30 + "\n")    