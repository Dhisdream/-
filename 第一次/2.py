import string

# 密文十六进制字符串
hex_ciphertext = 'F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923C\
AB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF\
5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84C\
C931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D96\
3FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47E\
FD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5\
923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA\
36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63C\
ED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A8\
5A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250\
C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794'

# 将十六进制密文转换为字节数组
def hex_to_bytes(hex_str):
    return [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

# 找出将密文解密成可见字符的所有可能密钥值
def possible_keys_for_segment(segment, visible_chars):
    possible_keys = list(range(0x00, 0xFF))
    for key in possible_keys[:]:
        for byte in segment:
            if chr(byte ^ key) not in visible_chars:
                possible_keys.remove(key)
                break
    return possible_keys

# 主程序
def main():
    # 定义可见字符集
    visible_chars = string.ascii_letters + string.digits + ',. '

    # 将十六进制密文转换为字节数组
    ciphertext_bytes = hex_to_bytes(hex_ciphertext)

    # 假设密钥长度为7
    key_length = 7

    # 存储每个位置的可能密钥
    vigenere_possible_keys = []

    # 尝试找出密钥
    for index in range(key_length):
        segment = [ciphertext_bytes[i] for i in range(index, len(ciphertext_bytes), key_length)]
        keys = possible_keys_for_segment(segment, visible_chars)
        vigenere_possible_keys.append(keys)

    # 尝试解密密文
    plaintext = ''
    for i, byte in enumerate(ciphertext_bytes):
        # 假设每个位置的密钥相同，取第一个可能的密钥
        possible_key = vigenere_possible_keys[i % key_length][0] if vigenere_possible_keys[i % key_length] else 0
        plaintext += chr(byte ^ possible_key)

    print("解密后的明文:", plaintext)

if __name__ == "__main__":
    main()