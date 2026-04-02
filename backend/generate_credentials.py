"""
SPPU Study Portal - Security Helper Script
==========================================
This script helps you generate secure credentials for your .env file

Usage:
    python generate_credentials.py
"""

import secrets
import bcrypt
import sys

def generate_secret_key():
    """Generate a secure random secret key for Flask"""
    return secrets.token_hex(32)

def generate_password_hash(password):
    """Generate a bcrypt hash for a password"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def main():
    print("=" * 60)
    print("🔐 SPPU Study Portal - Security Credentials Generator")
    print("=" * 60)
    print()
    
    # Generate Secret Key
    print("1️⃣  Generating Flask SECRET_KEY...")
    secret_key = generate_secret_key()
    print(f"   ✅ SECRET_KEY={secret_key}")
    print()
    
    # Generate Password Hash
    print("2️⃣  Generate Admin Password Hash")
    print("   Enter your desired admin password (or press Enter to skip):")
    password = input("   Password: ").strip()
    
    if password:
        print("   Generating bcrypt hash...")
        password_hash = generate_password_hash(password)
        print(f"   ✅ ADMIN_PASSWORD_HASH={password_hash}")
        print()
        print("   ⚠️  IMPORTANT: Use the hash above in your .env file")
        print("   ⚠️  Remove ADMIN_PASSWORD from .env for better security")
    else:
        print("   ⏭️  Skipped password hash generation")
    
    print()
    print("=" * 60)
    print("📝 Next Steps:")
    print("=" * 60)
    print("1. Copy the SECRET_KEY above to your .env file")
    if password:
        print("2. Copy the ADMIN_PASSWORD_HASH to your .env file")
        print("3. Remove or comment out ADMIN_PASSWORD in .env")
        print("4. Keep your .env file secure and never commit it to Git")
    else:
        print("2. Run this script again to generate password hash")
    print()
    print("✨ Your credentials are ready for production use!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
