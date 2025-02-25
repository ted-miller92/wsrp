import bcrypt
from zlib import crc32

# Define users and their new passwords
users = {
    "rwilson": "password123",
    "lchen": "password456",
    "dthomas": "ezpass",
    "jsmith": "easierpass",
    "sjohnson": "securepass",
    "mbrown": "superpass"
}

# Generate new hashes
for user, password in users.items():
    # Generate bcrypt hash
    bcrypt_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    # Generate CRC32 hash
    crc32_hash = format(crc32(password.encode('utf-8')) & 0xFFFFFFFF, '08x')

    print(f"('{user}', '{password}', '{crc32_hash}', '{bcrypt_hash}'),")
