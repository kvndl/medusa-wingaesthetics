import os
import requests
import re

# API endpoint to fetch product data
api_url = "https://cdn5.editmysite.com/app/store/api/v28/editor/users/147218291/sites/708783011253490589/products?page=1&per_page=120&sort_by=name&sort_order=asc&include=images"

# Create a session
session = requests.Session()

# Function to sanitize filenames by removing percentage signs
def sanitize_filename(name):
    return re.sub(r'[%]', '', name)

# Function to download images
def download_image(img_url, folder_path, img_name):
    try:
        response = session.get(img_url)
        response.raise_for_status()
        with open(os.path.join(folder_path, img_name), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {img_name}")
    except requests.RequestException as e:
        print(f"Failed to download {img_url}: {e}")

# Function to scrape images from the API
def scrape_images_from_api(api_url):
    try:
        response = session.get(api_url)
        response.raise_for_status()
        data = response.json()
        products = data.get('data', [])  # Accessing the 'data' key
        # Print only the first few products for sharing
        print("First few products JSON:", products[:3])
    except requests.RequestException as e:
        print(f"Failed to retrieve the products: {e}")
        return

    if not products:
        print("No products found in the response.")
        return

    for product in products:
        try:
            product_name = sanitize_filename(product['name'].strip())
            print(f"Scraping product: {product_name}")
        except KeyError as e:
            print(f"Failed to extract product information: {e}")
            continue

        # Create a folder for the product
        folder_path = os.path.join('products', product_name)
        os.makedirs(folder_path, exist_ok=True)

        # Download the thumbnail image
        thumbnail_url = product.get('thumbnail', {}).get('data', {}).get('url')
        if thumbnail_url:
            img_name = "thumbnail.jpg"
            download_image(thumbnail_url, folder_path, img_name)

        # Download all images in the images.data array
        images = product.get('images', {}).get('data', [])
        if not images:
            print(f"No images found for product: {product_name}")
            continue

        for idx, img in enumerate(images):
            try:
                img_url = img['url'].split('?')[0]  # Removing query parameters to get the original image
                img_name = f"{product_name}_{idx + 1}.jpg"
                download_image(img_url, folder_path, img_name)
            except KeyError as e:
                print(f"Failed to extract image URL: {e}")

if __name__ == "__main__":
    os.makedirs('products', exist_ok=True)
    scrape_images_from_api(api_url)
