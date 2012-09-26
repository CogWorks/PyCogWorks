import json
import datetime
from Crypto.Cipher import AES

def rin2id(rin):
    try:
        rin = int(rin)
        rin = '%s%s' % (str(rin), str(rin)[:7])
        cipher = AES.new(rin, AES.MODE_CBC, "0000000000000000")
        return ''.join(["%02x" % ord(x) for x in cipher.encrypt(rin)]).strip()
    except ValueError:
        raise Exception("Invalid RIN.")

def getDateTimeStamp():
    d = datetime.datetime.now().timetuple()
    return "%d-%d-%d_%d-%d-%d" % (d[0], d[1], d[2], d[3], d[4], d[5])
    
def writeHistoryFile(filename, subjectInfo):
    if 'rin' in subjectInfo:
        rin = subjectInfo['rin']
        if len(rin) != 9:
            raise Exception("The 'rin' field value must have a length of 9.")
        eid = rin2id(rin)
        if 'encrypted_rin' in subjectInfo and subjectInfo['encrypted_rin'] != eid:
            raise Exception("Invalid 'encrypted_rin' value for given 'rin'.")
        else:
            subjectInfo['encrypted_rin'] = eid
            subjectInfo['cipher'] = 'AES/CBC (RIJNDAEL) - 16Byte Key'
        history = open(filename, 'w')
        history.write(json.dumps(subjectInfo, sort_keys=True, indent=4))
        history.close()
    else:
        raise Exception("The 'subjectInfo' dict must contain a 'rin' field!")