import base64


def convert_hex_to_base64(hex_str):
    """
    将十六进制字符串转换为Base64编码的字符串。

    参数:
    hex_str (str): 十六进制字符串。

    返回:
    str: 对应的Base64编码字符串。
    """
    # 将十六进制字符串转换为字节
    raw_bytes = bytes.fromhex(hex_str)
    # 将字节转换为Base64编码并解码为UTF-8字符串
    base64_encoded = base64.b64encode(raw_bytes).decode('utf-8')
    return base64_encoded


# 主程序
def main():
    # 定义一个十六进制字符串
    hex_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
    # 调用函数进行转换
    base64_string = convert_hex_to_base64(hex_string)
    # 打印转换后的Base64字符串
    print("Base64编码:", base64_string)


if __name__ == '__main__':
    main()