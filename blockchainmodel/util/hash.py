from hashlib import sha256


def hash2(src):
    """
    两次hash，用于挖矿中hash头的生成
    :param src:<str> 要进行hash的字符串
    :return:hash结束的字符串
    """
    src_bytes = bytes.fromhex(src)
    hash1 = sha256(src_bytes).digest()
    result = sha256(hash1).hexdigest()
    return result


def byte2hex(b):
    """
    将byte类型的数值或字符串转换为16进制
    :return:返回十六进制字符串
    """
    return hex(int(b))[2:]


def hash_proof(proof):
    # 将随机值进行Hash
    hex_proof = byte2hex(proof)
    lens_sub = 8 - len(hex_proof)
    if lens_sub <= 0:
        return hex_proof[:8]
    return "0" * lens_sub + hex_proof
