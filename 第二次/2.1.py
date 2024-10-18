def pad(raw: bytes, block_size: int) -> bytes:
    if not (1 <= block_size <= 256):
        raise ValueError("Block size must be between 1 and 256")

    padding = block_size - (len(raw) % block_size)
    padding_byte = bytes([padding])
    return raw + (padding_byte * padding)

# Example usage:
data = b"Hello, World!"
block_size = 16
padded_data = pad(data, block_size)
print("Padded Data:", padded_data)
print("Length of Padded Data:", len(padded_data))