import secrets

def generate_token() -> str:
    return secrets.token_hex(20)  # Generates a 40-character hexadecimal token
