"""
SPPU Study Portal - Quick Setup Script
======================================
This script helps you set up your .env file quickly

Usage:
    python setup.py
"""

import os
import secrets
import shutil

def create_env_file():
    """Create .env file from .env.example"""
    
    print("=" * 60)
    print("🚀 SPPU Study Portal - Quick Setup")
    print("=" * 60)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("   Do you want to overwrite it? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("   Setup cancelled.")
            return
        print()
    
    # Copy .env.example to .env
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
    else:
        print("❌ .env.example not found!")
        return
    
    print()
    print("=" * 60)
    print("📝 Configuration Steps")
    print("=" * 60)
    print()
    
    # Generate SECRET_KEY
    print("1️⃣  Generating SECRET_KEY...")
    secret_key = secrets.token_hex(32)
    
    # Read .env file
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace SECRET_KEY
    content = content.replace(
        'SECRET_KEY=your-secret-key-here-change-this-in-production-use-64-character-random-string',
        f'SECRET_KEY={secret_key}'
    )
    
    # Write back
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("   ✅ SECRET_KEY generated and saved")
    print()
    
    # MongoDB URI
    print("2️⃣  MongoDB Configuration")
    print("   You need to set up MongoDB Atlas (cloud database)")
    print()
    print("   📚 Follow the guide: MONGODB_SETUP.md")
    print("   🔗 Quick start: https://www.mongodb.com/cloud/atlas")
    print()
    print("   After creating your MongoDB Atlas cluster:")
    print("   1. Get your connection string")
    print("   2. Open the .env file")
    print("   3. Replace the MONGODB_URI value with your connection string")
    print()
    
    # Admin credentials
    print("3️⃣  Admin Credentials")
    print("   Default admin credentials are set in .env:")
    print("   - Username: Pratik")
    print("   - Password: @Pratik9890")
    print()
    print("   ⚠️  IMPORTANT: Change these before deploying to production!")
    print("   💡 Run 'python generate_credentials.py' to create secure credentials")
    print()
    
    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print("   1. Set up MongoDB Atlas (see MONGODB_SETUP.md)")
    print("   2. Update MONGODB_URI in .env file")
    print("   3. Install dependencies: pip install -r requirements.txt")
    print("   4. Run the app: python app.py")
    print()
    print("📚 Documentation:")
    print("   - README.md - Complete project documentation")
    print("   - MONGODB_SETUP.md - MongoDB Atlas setup guide")
    print("   - DEPLOYMENT.md - Deployment instructions")
    print()
    print("🎉 Happy coding!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        create_env_file()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
