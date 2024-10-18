import re
import base64

def calculate_english_score(text):
    """评估文本是否为英文，基于字符频率分布"""
    # 字符频率分布
    freq_dist = {
        'a': 0.0651738, 'b': 0.0124248, 'c': 0.0217339, 'd': 0.0349835,
        'e': 0.1041442, 'f': 0.0197881, 'g': 0.0158610, 'h': 0.0492888,
        'i': 0.0558094, 'j': 0.0009033, 'k': 0.0050529, 'l': 0.0331490,
        'm': 0.0202124, 'n': 0.0564513, 'o': 0.0596302, 'p': 0.0137645,
        'q': 0.0008606, 'r': 0.0497563, 's': 0.0515760, 't': 0.0729357,
        'u': 0.0225134, 'v': 0.0082903, 'w': 0.0171272, 'x': 0.0013692,
        'y': 0.0145984, 'z': 0.0007836, ' ': 0.1918182
    }
    score = sum(freq_dist.get(char, 0) for char in text.lower())
    return score


def calculate_hamming_distance(str1, str2):
    """计算两个字符串之间的汉明距离"""
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))


def find_best_key_char(hex_values):
    """找到最有可能的单字符密钥"""
    best_key = ''
    best_score = 0
    for key_candidate in range(256):
        decrypted_text = ''.join(chr(key_candidate ^ int(hex_value, 16)) for hex_value in hex_values)
        score = calculate_english_score(decrypted_text)
        if score > best_score:
            best_score = score
            best_key = chr(key_candidate)
    return best_key


def main():
    # 读取并解码文件内容
    with open("6.txt", "r") as file:
        base64_lines = [line.strip() for line in file]
    decoded_content = "".join(base64.b64decode(line).decode('latin1') for line in base64_lines)

    # 估计密钥长度
    key_length_candidates = []
    for key_size in range(1, 41):
        blocks = [decoded_content[i:i + key_size] for i in range(0, len(decoded_content), key_size)][:4]
        if len(blocks) == 4:
            distances = [
                calculate_hamming_distance(blocks[0], blocks[1]),
                calculate_hamming_distance(blocks[1], blocks[2]),
                calculate_hamming_distance(blocks[2], blocks[3]),
                calculate_hamming_distance(blocks[0], blocks[2]),
                calculate_hamming_distance(blocks[0], blocks[3]),
                calculate_hamming_distance(blocks[1], blocks[3]),
            ]
            avg_distance = sum(distances) / len(distances)
            key_length_candidates.append((key_size, avg_distance))

    # 找到平均汉明距离最小的密钥长度
    key_length_candidates.sort(key=lambda x: x[1])
    print("Top 10 key lengths and average Hamming distances:")
    for candidate in key_length_candidates[:10]:
        print(f"Key length: {candidate[0]}, Avg Hamming distance: {candidate[1]}")

    # 解密密文
    hex_content = decoded_content.encode('latin1').hex()
    blocks = [re.findall(r'(.{2})', hex_part) for hex_part in re.findall(r'(.{58})', hex_content)]
    key = ''.join(find_best_key_char(block_column) for block_column in zip(*blocks))

    # 使用找到的密钥解密
    repeated_key = (key * ((len(decoded_content) // len(key)) + 1))[:len(decoded_content)]
    decrypted_message = ''.join(chr(ord(decoded_content[i]) ^ ord(repeated_key[i])) for i in range(len(decoded_content)))

    print(f"Derived key: {key}")
    print(f"Decrypted message:\n{decrypted_message}")


if __name__ == '__main__':
    main()