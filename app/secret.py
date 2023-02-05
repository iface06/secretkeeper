import datetime
import json
import uuid
from base64 import b64encode
from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class Secret:
    def __init__(self, name, fact, tags):
        self.name = name
        self.fact = fact
        self.tags = tags
        self.created = datetime.datetime.now()
        self.id = uuid.uuid4()


class JsonsEncryptor:
    def __init__(self, factEncryptionAlogrithm, factSignatureAlgorithm):
        self.payloadEncryptionAlogrithm = factEncryptionAlogrithm
        self.payloadSignatureAlgorithm = factSignatureAlgorithm

    def toJsons(self, secret, key=''):
        if not key:
            key = self.payloadEncryptionAlogrithm.generateKey()
        jsons = {
            'header': {
                'name': secret.name,
                'tags': secret.tags,
                'created': secret.created.strftime('%Y-%M-%dT%H:%M:%S.%fZ%z'),
                'encryptionAlgorithm': self.payloadEncryptionAlogrithm.algorithm,
                'signature': self.payloadSignatureAlgorithm.sign(secret.fact, key),
                'signatureAlgorithm': self.payloadSignatureAlgorithm.algorithm,
                'id': str(secret.id)
            },
            'fact': self.payloadEncryptionAlogrithm.encrypt(secret.fact, key)
        }
        return json.dumps(jsons), key

class FactEncryptionAlgorithm:
    def __init__(self):
        self.algorithm = 'AES256'
        self.bytesForKey = 16 #Bytes: 16 for 128AES; 24 for 190AES, 32 for 256AES
        self.stringLengthOfBase64CodedByteKey = 172 #String Length (base64/utf-8) 256, 344

    def encrypt(self, fact, base64BasedKey):
        encryptedFact = ''
        if base64BasedKey:
            byteKey = b64decode(base64BasedKey)
            cipher = AES.new(byteKey, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(str.encode(fact))
            encryptedFact = EncryptedFact(cipher.nonce, ciphertext, tag).toJson()
        return encryptedFact

    def generateKey(self):
        byteKey = get_random_bytes(self.bytesForKey)
        return b64encode(byteKey).decode('utf-8')

class EncryptedFact:

    def __init__(self, nonce, ciphertext, tag):
        self.nonce = nonce
        self.ciphertext = ciphertext
        self.tag = tag

    def toJson(self):
        return self.encodeInBase64(bytes(json.dumps(
            {
                'nonce': self.encodeInBase64(self.nonce),
                'ciphertext': self.encodeInBase64(self.ciphertext),
                'tag': self.encodeInBase64(self.tag)
            }
        ), 'utf-8'))

    def encodeInBase64(self, txt):
        return b64encode(txt).decode('utf-8')

    def decodeBase64(self, txt):
        return b64decode(txt)


class JsonsDecryptor:
    def __init__(self, factDecryptionAlgorithm):
        self.factDecryptionAlgorithm = factDecryptionAlgorithm

    def toSecret(self, jsons, key):
        jsonObj = jsons
        if isinstance(jsons, str):
            jsonObj = json.loads(jsons)

        encryptedFact = self.encryptedFactFromJson(jsonObj['fact'])
        fact = self.factDecryptionAlgorithm.decryption(encryptedFact, key)
        return Secret(jsonObj['header']['name'], fact, jsonObj['header']['tags'])

    def encryptedFactFromJson(self, jsonRepresentation):
        jsonObj = json.loads(b64decode(jsonRepresentation))
        return EncryptedFact(
            b64decode(jsonObj['nonce']),
            b64decode(jsonObj['ciphertext']),
            b64decode(jsonObj['tag'])
        )

class FactDecryptionAlgorithm:
    def __init__(self):
        self.algorithm = 'AES256'

    def decryption(self, encryptedSecret, key):
        cipher = AES.new(b64decode(key), AES.MODE_EAX, encryptedSecret.nonce)
        plaintext = cipher.decrypt_and_verify(encryptedSecret.ciphertext, encryptedSecret.tag)
        return plaintext.decode()


class FactSignatureAlgorithm:
    def __init__(self):
        self.algorithm = 'pytonHash'

    def sign(self, fact, key):
        return hash(fact + key)