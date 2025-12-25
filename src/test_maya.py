import requests
from requests.auth import HTTPBasicAuth
import json

def test_maya_api():
    # Credentials from user screenshot
    API_KEY = "YUq15J3kizpf"
    API_SECRET = "bgiSXZ1qoh9JOzj8N28sB0u1IeaNb3dQGMn6cfYrgLDyr5vLMAzdJVDxFkOtmv3i"
    URL = "https://api.maya.net/partners/v1/products"

    try:
        print(f"Connecting to {URL}...")
        response = requests.get(
            URL, 
            auth=HTTPBasicAuth(API_KEY, API_SECRET)
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            # Save a sample to inspect structure
            with open("maya_response_sample.json", "w") as f:
                json.dump(data, f, indent=4)
            
            print("Success! Data saved to maya_response_sample.json")
            
            # Print a sneak peek
            if "products" in data:
                count = len(data["products"])
                print(f"Found {count} products.")
                if count > 0:
                    print("First product sample:")
                    print(json.dumps(data["products"][0], indent=2))
        else:
            print("Error Response:")
            print(response.text)

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_maya_api()
