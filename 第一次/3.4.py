import re

def xor_decrypt(hex_str, key):
    """使用给定的密钥对十六进制字符串进行XOR解密"""
    return ''.join(chr(int(hex_str[i:i+2], 16) ^ key) for i in range(0, len(hex_str), 2))


def calculate_score(decrypted_str):
    """计算解密字符串的得分，基于字母和空格的数量"""
    return len(re.findall(r'[a-zA-Z ]', decrypted_str))


def find_best_key(hex_str):
    """找到解密十六进制字符串的最佳密钥"""
    best_score = 0
    best_key = ''
    best_decrypted_str = ''

    for potential_key in range(0, 129):
        decrypted_str = xor_decrypt(hex_str, potential_key)
        score = calculate_score(decrypted_str)

        if score > best_score:
            best_score = score
            best_decrypted_str = decrypted_str
            best_key = chr(potential_key)

    return best_key, best_decrypted_str, best_score


def main():
    # 读取文件中的每一行，并去掉换行符
    with open("4.txt", "r") as file:
        hex_lines = file.read().splitlines()

    overall_best_score = 0
    overall_best_line = ''
    overall_best_decrypted_str = ''
    overall_best_key = ''

    # 遍历文件中的每一行，逐行解密
    for hex_line in hex_lines:
        key, decrypted_str, score = find_best_key(hex_line)

        if score > overall_best_score:
            overall_best_score = score
            overall_best_line = hex_line
            overall_best_decrypted_str = decrypted_str
            overall_best_key = key

    # 输出解密结果
    print(f"Original hex line: {overall_best_line}")
    print(f"Key: {overall_best_key}")
    print(f"Decrypted message: {overall_best_decrypted_str}")


if __name__ == '__main__':
    main()