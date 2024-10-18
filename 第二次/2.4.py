import base64
import os
from Crypto.Cipher import AES
import string

# 添加PKCS#7填充
def add_padding(message: bytes, block_size: int) -> bytes:
    padding_size = block_size - (len(message) % block_size)
    return message + bytes([padding_size] * padding_size)

# 去除PKCS#7填充
def remove_padding(message: bytes) -> bytes:
    padding_size = message[-1]
    return message[:-padding_size]

# 使用AES ECB模式加密
def aes_ecb_encrypt(controlled_text: bytes) -> bytes:
    secret_key = os.urandom(16)
    payload = controlled_text + base64.b64decode("""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK""")
    padded_payload = add_padding(payload, AES.block_size)
    cipher = AES.new(secret_key, AES.MODE_ECB)
    return cipher.encrypt(padded_payload)

# 确定明文长度
def determine_plaintext_length() -> int:
    initial_length = len(aes_ecb_encrypt(b""))
    length = initial_length
    for i in range(16):
        encrypted = aes_ecb_encrypt(b"A" * i)
        if len(encrypted) != initial_length:
            length = initial_length - i
            break
    return length

# 深度优先搜索恢复明文
def dfs(known_text: bytes, plaintext_length: int) -> bool:
    if len(known_text) == plaintext_length:
        print(known_text.decode())
        return True
    possible_chars = string.printable.encode()
    for char in possible_chars:
        block_size = AES.block_size
        block_oracle = known_text[:block_size - 1] + bytes([char]) + b"\x00" * (block_size - len(known_text) % block_size - 1)
        encrypted_oracle = aes_ecb_encrypt(block_oracle)
        for i in range(16):
            if encrypted_oracle[i] == encrypted_oracle[len(known_text) // block_size * block_size + 15]:
                if dfs(known_text + bytes([char]), plaintext_length):
                    return True
    return False

# 主程序
def main():
    plaintext_length = determine_plaintext_length()
    dfs(b'', plaintext_length)

if __name__ == "__main__":
    main()