import requests

# Define the Medusa Admin API URL and your credentials
MEDUSA_API_URL = "https://medusa.noahschepers.com/admin"
EMAIL = "admin@medusa-test.com"
PASSWORD = "supersecret"

# Authenticate and get the access token
def get_access_token():
    auth_url = f"{MEDUSA_API_URL}/auth"
    auth_data = {
        "email": EMAIL,
        "password": PASSWORD
    }
    response = requests.post(auth_url, json=auth_data)

    # print(f"Response status: {response.status_code}")
    # print(f"Response text: {response.text}")
    
    if response.status_code == 200:
        return response.json()["user"]["api_token"]
    else:
        print(f"Failed to authenticate, Status Code: {response.status_code}, Response: {response.text}")
        return None

# Function to delete a product by ID
def delete_product(product_id, headers):
    response = requests.delete(f"{MEDUSA_API_URL}/products/{product_id}", headers=headers)
    if response.status_code == 200:
        print(f"Deleted product with ID: {product_id}")
    else:
        print(f"Failed to delete product with ID: {product_id}, Status Code: {response.status_code}, Response: {response.text}")

# Main script execution
def main():
    api_token = get_access_token()
    print(f"api token: {api_token}")
    
    if not api_token:
        return

    headers = {
        "x-medusa-access-token": api_token,
        "Content-Type": "application/json"
    }

    # Get the list of all products
    response = requests.get(f"{MEDUSA_API_URL}/products", headers=headers)

    # print(f"Request Headers: {headers}")
    # print(f"Response status: {response.status_code}")
    # print(f"Response text: {response.text}")

    if response.status_code == 200:
        products = response.json().get('products', [])
        # Loop through each product ID and delete the product
        for product in products:
            delete_product(product['id'], headers)
        print("All products have been deleted.")
    else:
        print(f"Failed to retrieve products, Status Code: {response.status_code}, Response: {response.text}")

if __name__ == "__main__":
    main()
