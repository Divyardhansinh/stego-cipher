from PIL import Image

# 16-bit delimiter to mark end of message
DELIMITER = '1111111111111110'

def text_to_binary(data: str) -> str:
    """Convert string to binary representation."""
    return ''.join(format(ord(char), '08b') for char in data)

def binary_to_text(binary: str) -> str:
    """Convert binary string to text."""
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def embed_bits_in_pixels(pixels, bits: str):
    """Embed bits into pixel LSBs (RGB channels only)."""
    bits += DELIMITER
    bit_index = 0
    max_bits = len(bits)
    
    for i in range(len(pixels)):
        if bit_index >= max_bits:
            break
        pixel = list(pixels[i])
        for j in range(min(3, len(pixel))):  # RGB only
            if bit_index >= max_bits:
                break
            pixel[j] = (pixel[j] & ~1) | int(bits[bit_index])
            bit_index += 1
        pixels[i] = tuple(pixel)
    
    return pixels

def extract_bits_from_pixels(pixels) -> str:
    """Extract bits from pixel LSBs until delimiter is found."""
    bits = ''
    for pixel in pixels:
        for channel in pixel[:3]:  # Only RGB
            bits += str(channel & 1)
            if len(bits) >= len(DELIMITER) and bits[-len(DELIMITER):] == DELIMITER:
                return bits[:-len(DELIMITER)]
    raise ValueError("No hidden message found (delimiter missing).")

def hide_message(image_path: str, message: str, output_path: str):
    """Hide message in ANY image format by converting to PNG internally."""
    # Open and convert to RGBA (supports RGB + transparency safely)
    img = Image.open(image_path).convert('RGBA')
    pixels = list(img.getdata())
    
    binary_message = text_to_binary(message)
    available_bits = len(pixels) * 3
    required_bits = len(binary_message) + len(DELIMITER)
    
    if required_bits > available_bits:
        max_chars = (available_bits - len(DELIMITER)) // 8
        raise ValueError(
            f"Message too large! Max: {max_chars} characters. "
            f"Your message: {len(message)} chars."
        )
    
    # Embed data
    modified_pixels = embed_bits_in_pixels(pixels, binary_message)
    img.putdata(modified_pixels)
    # ALWAYS save as PNG to prevent data loss
    img.save(output_path, "PNG")

def reveal_message(image_path: str) -> str:
    """Reveal message from image (should be PNG for reliable results)."""
    # Warn if non-PNG is used
    if not image_path.lower().endswith('.png'):
        print("⚠️  Warning: Non-PNG image detected. Hidden data may be corrupted!")
    
    img = Image.open(image_path)
    # Work in RGB/RGBA to avoid mode issues
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGBA')
    pixels = list(img.getdata())
    
    binary_message = extract_bits_from_pixels(pixels)
    return binary_to_text(binary_message)