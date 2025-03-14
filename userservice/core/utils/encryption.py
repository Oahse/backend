from argon2 import PasswordHasher

class PasswordManager:
    def __init__(self):
        # Initialize Argon2 PasswordHasher
        self.ph = PasswordHasher()

    # Hashing a password
    def hash_password(self, password: str) -> str:
        return self.ph.hash(password)

    # Verifying a password
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        try:
            # Verify the hashed password against the input password
            self.ph.verify(hashed_password, plain_password)
            return True
        except Exception as e:
            # Return False if an error occurs (e.g., password doesn't match)
            return False


# Example usage
# password_manager = PasswordManager()

# # Hash a password
# password = "user_password"
# hashed_password = password_manager.hash_password(password)
# print("Hashed Password:", hashed_password)

# # Verifying the password
# is_correct = password_manager.verify_password(password, hashed_password)
# print("Password Verified:", is_correct)

# # Trying to verify with a wrong password
# is_correct_wrong = password_manager.verify_password("wrong_password", hashed_password)
# print("Password Verified (with wrong password):", is_correct_wrong)
