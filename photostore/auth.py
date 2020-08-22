
class Auth():
    """Simple auth module (really simple)"""

    def __init__(self, secret_keys_filename: str, token_validity_duration_ms: int = 60000):
        with open(secret_keys_filename) as secret_keys_file:
            self.secret_keys = secret_keys_file.read().split('\n')

    def is_valid(self, secret_key: str):
        return secret_key in self.secret_keys

