from Crypto.Cipher import AES

def rin2id(rin):
    rin = '%s%s' % (rin,rin[:7])
    cipher = AES.new(rin, AES.MODE_CBC, "0000000000000000")
    return ''.join(["%02x" % ord(x) for x in cipher.encrypt(rin)]).strip()