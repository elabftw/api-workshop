import requests
import urllib3

# ==========================
# 🔧 CONFIGURATION
# ==========================
API_HOST_URL = 'https://YOUR_HOST_URL/api/v2'  # <-- Replace with your instance URL 
API_KEY = 'YOUR_API_KEY'  # <-- Replace with your API key

CATEGORY_ID = 19  # <-- Replace with desired resource category ID

# Disable warnings for self-signed SSL certificates (optional)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {
    "Authorization": API_KEY,
    "Accept": "application/json"
}

# ==========================
# 📋 LIST RESOURCE CATEGORIES
# ==========================
print("📋 Loading resource categories (IDs only)...")

try:
    response = requests.get(f"{API_HOST_URL}/items_types", headers=headers, verify=False)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, dict):
        categories = data.get("items", data.get("data", []))
    else:
        categories = data

    print("📂 Available category IDs:")
    for cat in categories:
        print(f"- Category ID: {cat.get('id')}")

except Exception as e:
    print(f"❌ Error while retrieving categories: {e}")

# ==========================
# 📊 COUNT ENTRIES
# ==========================
print(f"\n📊 Counting entries in category {CATEGORY_ID}...")

try:
    total_items = 0
    page = 1
    while True:
        response = requests.get(
            f"{API_HOST_URL}/items",
            headers=headers,
            params={"category_id": CATEGORY_ID, "page": page},
            verify=False
        )
        response.raise_for_status()
        items = response.json()

        if isinstance(items, dict):
            items = items.get("items", items.get("data", []))

        count = len(items)
        total_items += count

        if count < 50:
            break
        page += 1

    print(f"✅ Total entries in category {CATEGORY_ID}: {total_items}")

except Exception as e:
    print(f"❌ Error while counting items: {e}")
