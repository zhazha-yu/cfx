from gmssl import sm2

from Crypto.Util.number import *
from base64 import b64encode, b64decode


def encrypt(text, pubk='6e0b868cccf23842bce58726e860ea332ea836725fbbb461444e551c57c0d78d9863ef6a7fef50743d941f51bb40d49ab026bc77eede2b1ced0867fdc7ab7a19'):
    sm2_crypt = sm2.CryptSM2(public_key=pubk, private_key=0)
    text = sm2_crypt.encrypt(text.encode())
    text = b64encode(text).decode()
    return text


def decrypt(text, prik='a66875d2bd621a8214409b9e313f633a9bee056cf1cf3b09bec15c8232828b95'):
    sm2_crypt = sm2.CryptSM2(public_key=0, private_key=prik)
    text = sm2_crypt.decrypt(b64decode(text)).decode()
    return text

def file_encode(path):
    with open(path, 'rb') as f1:
        base64_str = b64encode(f1.read())  # base64类型
        src = base64_str.decode('utf-8')  # str
        src = encrypt(src)
        with open('%s'%path, 'w') as f2:
            f2.write(src)
            print('加密完成！')

def file_decode(path):
    with open(path,'rb') as f1:
        src = f1.read()
        src = decrypt(src)
        src = b64decode(src)
        with open('%s'%path, 'wb') as f2:
            f2.write(src)
            print('解密完成！')
