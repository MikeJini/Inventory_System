import requests

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
    requests.post('http://127.0.0.1:5000/api/products', json=item)