def xor_two_bytes(byte1, byte2):
    """对两个字节进行异或运算并返回结果"""
    return byte1 ^ byte2


def xor_bytes_str(bytes1, bytes2):
    """对两个等长的字节字符串进行逐字节异或运算并返回结果字符串"""
    return bytes(xor_two_bytes(b1, b2) for b1, b2 in zip(bytes1, bytes2))


if __name__ == '__main__':
    hex_str1 = '1c0111001f010100061a024b53535009181c'
    hex_str2 = '686974207468652062756c6c277320657965'

    # 将十六进制字符串转换为原始字节字符串
    raw_bytes1 = bytes.fromhex(hex_str1)
    raw_bytes2 = bytes.fromhex(hex_str2)

    # 对两个字节字符串进行异或操作
    xor_result_bytes = xor_bytes_str(raw_bytes1, raw_bytes2)

    # 将异或结果转换回十六进制表示
    final_hex_result = xor_result_bytes.hex()

    print(final_hex_result)