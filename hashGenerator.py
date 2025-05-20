import bcrypt

# Define users and their new passwords
users = {
    "rwilson": "password123",
    "lchen": "password456",
    "dthomas": "ezpass",
    "jsmith": "easierpass",
    "sjohnson": "securepass",
    "mbrown": "superpass"
}

# Generate new bcrypt hashes
for user, password in users.items():
    # Generate bcrypt hash
    bcrypt_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    print(f"('{user}', '{password}', '{bcrypt_hash}'),")


def calculate_bcrypt(password):
    """Calculate bcrypt hash of password"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


