import os
import sys

# Simplified entry point for production
try:
    from app import create_app
    app = create_app()
except ImportError as e:
    print(f"CRITICAL ERROR: Failed to import factory: {e}")
    sys.exit(1)

if __name__ == "__main__":
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
