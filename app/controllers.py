import app.secret as scrt
import app.secretFileStorage as strge

def store(secretDto):
    key = secretDto.key
    secret = scrt.Secret(secretDto.name, secretDto.fact, secretDto.tags)
    secretStorage = strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.')
    key = secretStorage.store(secret, key)
    return secret, key

def readSecret(name, key):
    secretStorage = strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()))
    secretFile = secretStorage.load(name)

    decryptor = scrt.JsonsDecryptor(scrt.FactDecryptionAlgorithm())
    secret = decryptor.toSecret(secretFile.read(), key)

    return secret

def listSecrets():
    return strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.').list()

def findSecretByTags(tags):
    return strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.').find(tags)

class SecretDto:
    def __init__(self, name, fact, key, tags):
        self.name = name
        self.fact = fact
        self.key = key
        self.tags = tags
