import os
import random
from Crypto.Cipher import AES


# 生成随机密钥
def generate_random_key() -> bytes:
    return os.urandom(16)


# 生成随机填充
def generate_random_padding(length: int = random.randint(5, 10)) -> bytes:
    return os.urandom(length)


# 添加PKCS#7填充
def add_padding(message: bytes, block_size: int) -> bytes:
    padding_size = block_size - (len(message) % block_size)
    return message + bytes([padding_size] * padding_size)


# 去除PKCS#7填充
def remove_padding(message: bytes) -> bytes:
    padding_size = message[-1]
    return message[:-padding_size]


# 加密预言机
def encryption_oracle(encryption_key: bytes, plaintext: bytes) -> (bytes, AES.MODE_ECB | AES.MODE_CBC):
    encryption_mode = random.choice([AES.MODE_ECB, AES.MODE_CBC])
    padded_plaintext = generate_random_padding() + plaintext + generate_random_padding()
    padded_plaintext = add_padding(padded_plaintext, AES.block_size)

    match encryption_mode:
        case AES.MODE_ECB:
            cipher = AES.new(encryption_key, encryption_mode)
            return cipher.encrypt(padded_plaintext), encryption_mode
        case AES.MODE_CBC:
            iv = generate_random_key()
            cipher = AES.new(encryption_key, encryption_mode, iv)
            return cipher.encrypt(padded_plaintext), encryption_mode
    assert False, "Unreachable code"


# 检测加密模式
def detect_encryption_mode(ciphertext: bytes) -> AES.MODE_ECB | AES.MODE_CBC:
    blocks = [ciphertext[i:i + 16] for i in range(0, len(ciphertext), 16)]
    if len(set(blocks)) != len(blocks):
        return AES.MODE_ECB
    return AES.MODE_CBC


# 主程序
def main():
    encryption_key = generate_random_key()
    test_plaintext = b"\x00" * (16 * 3)
    encrypted_samples = [encryption_oracle(encryption_key, test_plaintext) for _ in range(1000)]

    correct_detections = sum(
        1 for cipher_text, mode in encrypted_samples if detect_encryption_mode(cipher_text) == mode)
    accuracy = correct_detections / len(encrypted_samples)

    print(f"Accuracy of detecting encryption mode: {accuracy:.2%}")


if __name__ == "__main__":
    main()