import os
import re
from pathlib import Path
from crypto_utils import load_key, encrypt_message, decrypt_message
from stego_engine import hide_message, reveal_message

# Define folders
INPUT_DIR = Path("input_images")
OUTPUT_DIR = Path("output_stego")

def setup_directories():
    """Create input/output folders if they don't exist."""
    INPUT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

def clean_path(path: str) -> str:
    """Remove quotes and normalize Unicode spaces."""
    path = path.strip().strip("'\"")
    path = re.sub(r'[\u00A0\u202F\u2009\u200A\u2007\u2008]', ' ', path)
    return path

def main():
    setup_directories()
    key = load_key()
    
    print("=== Organized Steganography Tool ===")
    print(f"📁 Place original images in: {INPUT_DIR}")
    print(f"📤 Stego outputs saved to: {OUTPUT_DIR}")
    print("1. Hide message in an image (from input_images/)")
    print("2. Reveal message from a stego image (from output_stego/)")
    
    choice = input("Select option (1/2): ").strip()
    
    if choice == "1":
        filename = input(f"Enter filename (e.g., photo.jpg) from '{INPUT_DIR}': ").strip()
        input_path = INPUT_DIR / filename
        
        if not input_path.exists():
            print(f"❌ File not found: {input_path}")
            print(f"👉 Make sure '{filename}' is inside the '{INPUT_DIR}' folder.")
            return
        
        message = input("Enter secret message: ")
        # Output always PNG, saved in output_stego/
        output_filename = f"stego_{Path(filename).stem}.png"
        output_path = OUTPUT_DIR / output_filename
        
        try:
            encrypted = encrypt_message(message, key)
            encrypted_str = encrypted.decode('latin-1')
            hide_message(str(input_path), encrypted_str, str(output_path))
            print(f"✅ Success! Saved to: {output_path}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    elif choice == "2":
        filename = input(f"Enter stego filename (e.g., stego_photo.png) from '{OUTPUT_DIR}': ").strip()
        output_path = OUTPUT_DIR / filename
        
        if not output_path.exists():
            print(f"❌ File not found: {output_path}")
            print(f"👉 Make sure '{filename}' is inside the '{OUTPUT_DIR}' folder.")
            return
        
        try:
            encrypted_str = reveal_message(str(output_path))
            encrypted_bytes = encrypted_str.encode('latin-1')
            decrypted = decrypt_message(encrypted_bytes, key)
            print(f"🔓 Decrypted message: {decrypted}")
        except ValueError:
            print("📭 No hidden message found in this image.")
        except Exception as e:
            print(f"❌ Failed to reveal/decrypt: {e}")
    else:
        print("❌ Invalid option!")

if __name__ == "__main__":
    main()