from Crypto.Cipher import Blowfish

def rin2id(rin):
    rin = '%s%s' % (rin,rin[:7])
    cipher = Blowfish.new(rin, Blowfish.MODE_CBC, "00000000")
    return ''.join(["%02x" % ord(x) for x in cipher.encrypt(rin)]).strip()