import requests
import base64
from config import Config

# Step 1: Get an access token
def get_access_token():
    url = Config.ZOOM_AUTH_URL
    auth_string = f"{Config.ZOOM_CLIENT_ID}:{Config.ZOOM_CLIENT_SECRET}"
    auth_encoded = base64.b64encode(auth_string.encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth_encoded}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    # URL-encoded form data
    data = f"grant_type=account_credentials&account_id={Config.ZOOM_ACCOUNT_ID}"
    
    # Debug output (commented out by default for security)
    # print("\n🔍 Debug Info:")
    # print(f"Account ID: {Config.ZOOM_ACCOUNT_ID}")
    # print(f"Client ID: {Config.ZOOM_CLIENT_ID}")
    # print(f"Auth Header: Basic {'*' * 20}")
    # print(f"Request Data: {data}\n")
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print("❌ Failed to fetch token:")
        print(f"Error: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Status: {e.response.status_code}")
            print(f"Response: {e.response.text}")
        raise

# Step 2: Assign license by setting type=2 (Licensed user)
def assign_license(user_email, license_type=2):
    """
    Assign a Zoom license to a user
    
    Args:
        user_email (str): Email of the user to assign license to
        license_type (int, optional): Type of license to assign. Defaults to 2 (Licensed user).
                                     1: Basic (Free)
                                     2: Licensed (Paid)
                                     3: On-premise
    """
    token = get_access_token()
    url = f"https://api.zoom.us/v2/users/{user_email}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Payload to assign a license (type=2 for Licensed user)
    payload = {
        "type": license_type
    }

    try:
        response = requests.patch(url, headers=headers, json=payload)
        if response.status_code == 204:
            print(f"✅ License assigned successfully for {user_email}")
            return True
        else:
            print(f"❌ Failed to assign license: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error assigning license: {str(e)}")
        return False

if __name__ == "__main__":
    # Example usage:
    # assign_license("user@example.com", license_type=2)  # Assign Licensed user
    assign_license(Config.DEFAULT_USER_EMAIL)
