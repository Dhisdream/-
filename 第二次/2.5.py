from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 固定的 AES 密钥
ENCRYPTION_KEY = b"\xc6\xfe\xe2/\x97r|/\xeaY\x85C\xbfi\x99\x97"

# 加密函数
def encrypt_user_data(user_data: bytes) -> bytes:
    # 清洗用户数据
    sanitized_data = user_data.replace(b"&", b"").replace(b"=", b"")
    formatted_data = b"userdata=" + sanitized_data + b"&uid=10&role=user"

    # 添加填充并加密
    padded_data = pad((b"\x00" * 16) + formatted_data, 16)
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    return cipher.encrypt(padded_data)

# 解密函数
def decrypt_user_data(encrypted_data: bytes) -> dict:
    # 解密并去除填充
    cipher = AES.new(ENCRYPTION_KEY, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    unpadded_data = unpad(decrypted_data, 16)[16:]

    # 解析键值对
    return {
        (key_value := item.split(b"=", maxsplit=1))[0].decode(): key_value[1].decode()
        for item in unpadded_data.split(b"&")
    }

# 判断用户是否为管理员
def is_admin_user(encrypted_data: bytes) -> bool:
    decrypted = decrypt_user_data(encrypted_data)
    print(decrypted)
    return decrypted.get("role") == "admin"

# 主程序
def main():
    # 构造攻击数据
    user_data_to_inject = b"A" * 7 + b"admin" + b"\x0b" * 14
    encrypted_data = encrypt_user_data(user_data_to_inject)

    # 篡改密文
    modified_encrypted_data = encrypted_data[:64] + encrypted_data[32:48]

    # 检查是否成功成为管理员
    assert is_admin_user(modified_encrypted_data), "Failed to gain admin privileges"

if __name__ == "__main__":
    main()