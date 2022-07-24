import datetime
import json

class FactSignatureAlgorithm:
    def sign(self, secret, key):
        return hash(secret.fact + key)

class FactEncryptionAlgorithm:
    def encrypt(self, secret, key):
        return secret.fact

class JsonsEncryptor:
    def __init__(self, factEncryptionAlogrithm, factSignatureAlgorithm):
        self.payloadEncryptionAlogrithm = factEncryptionAlogrithm
        self.payloadSignatureAlgorithm = factSignatureAlgorithm

    def toJson(self, secret, key):
        jsons = {
            'header': {
                'name': secret.name,
                'tags': secret.tags,
                'created': secret.created.strftime('%Y-%M-%dT%H:%M:%S.%fZ%z'),
                'algorithm': 'AES256',
                'signature': self.payloadSignatureAlgorithm.sign(secret, key)
            },
            'fact': self.payloadEncryptionAlogrithm.encrypt(secret, key)
        }
        return json.dumps(jsons)

class Secret:
    def __init__(self, name, fact, tags):
        self.name = name
        self.fact = fact
        self.tags = tags
        self.created = datetime.datetime.now()

class SecretFile:
    def __init__(self, secret, jsonsEncryptor):
        self.secret = secret
        self.jsonsEncryptor = jsonsEncryptor
    def writeEncryptedSecretToDisk(self, key):
        self.file = open(self.secret.name + '.jsons', 'wt')
        self.file.write(self.jsonsEncryptor.toJson(secret, key))
        self.file.close();



secret = Secret('systempasswordpdb','53cr3t', ['systemb', 'pdb'])
secretAsJson = JsonsEncryptor(FactEncryptionAlgorithm(), FactSignatureAlgorithm()).toJson(secret, '123321')
secretFile = SecretFile(secret, JsonsEncryptor(FactEncryptionAlgorithm(), FactSignatureAlgorithm()))
secretFile.writeEncryptedSecretToDisk('123123123')
file = open(secret.name + '.jsons', 'rt')
print('File Content: ' + file.read())
