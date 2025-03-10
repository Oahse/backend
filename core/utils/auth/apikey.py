import hashlib
import base64
import json
from datetime import datetime, timedelta
from typing import List

class APIKeyGenerator:
    @staticmethod
    def generate_api_key(user_id: str, roles: List[str], expires_in: timedelta = timedelta(hours=1)) -> str:
        """
        Generates an API key using user ID, roles, and expiration date.
        :param user_id: The unique identifier of the user
        :param roles: The roles associated with the user (as a list of strings)
        :param expires_in: The expiration duration of the API key
        :return: A securely generated API key
        """
        
        # Combine user details and expiration info
        expiration_timestamp = (datetime.utcnow() + expires_in).timestamp()
        api_key_data = {
            'user_id': user_id,
            'roles': roles,
            'exp': expiration_timestamp,
            'timestamp': datetime.utcnow().timestamp()
        }

        # Convert the data to a string
        api_key_str = json.dumps(api_key_data, separators=(',', ':'))

        # Generate a SHA-256 hash of the combined string
        api_key_hash = hashlib.sha256(api_key_str.encode('utf-8')).hexdigest()

        # Optionally, encode the hash in base64 for readability and use
        api_key_base64 = base64.urlsafe_b64encode(api_key_hash.encode('utf-8')).decode('utf-8')

        return api_key_base64

    @staticmethod
    def verify_api_key(api_key: str, user_id: str, db_roles: List[str]) -> bool:
        """
        Verifies if the provided API key is valid and matches the user info.
        :param api_key: The API key string
        :param user_id: The user ID making the request
        :param db_roles: List of roles available for the user in the database
        :return: True if the key is valid and not expired, False otherwise
        """
        try:
            # Decode the base64-encoded API key
            decoded_key = base64.urlsafe_b64decode(api_key).decode('utf-8')
            
            # Convert the decoded string back to a dictionary
            api_key_data = json.loads(decoded_key)
            
            # Check if the user_id and roles match
            if api_key_data['user_id'] != user_id:
                return False
            
            if any(role not in db_roles for role in api_key_data['roles']):
                return False
            
            # Check if the key is expired
            if api_key_data['exp'] < datetime.utcnow().timestamp():
                return False
            
            return True
        except Exception as e:
            # In case of any decoding or data issues, return False
            return False

# user_id = "user123"
# roles = ["admin", "user"]
# expires_in = timedelta(hours=1)

# api_key = APIKeyGenerator.generate_api_key(user_id, roles, expires_in)
# print("Generated API Key:", api_key)

# api_key_to_verify = "the_api_key_received_in_the_request"
# user_id = "user123"
# db_roles = ["admin", "user"]  # The roles you retrieve from the database for the user

# is_valid = APIKeyGenerator.verify_api_key(api_key_to_verify, user_id, db_roles)
# if is_valid:
#     print("API key is valid.")
# else:
#     print("API key is invalid or expired.")
