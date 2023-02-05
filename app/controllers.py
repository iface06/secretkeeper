import app.secret as scrt
import app.secretFileStorage as strge

def store(secretDto):
    key = secretDto.key
    secret = scrt.Secret(secretDto.name, secretDto.fact, secretDto.tags)
    secretStorage = strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), secretDto.basepath)
    key = secretStorage.store(secret, key)
    return secret, key

def readSecret(name, key, basepath):
    secretStorage = strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), basepath)
    secretFile = secretStorage.load(name)

    decryptor = scrt.JsonsDecryptor(scrt.FactDecryptionAlgorithm())
    secret = decryptor.toSecret(secretFile, key)

    return secret

def listSecrets(basepath):
    return strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), basepath).list()

def findSecretByTags(tags, basepath):
    return strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), basepath).find(tags)

class SecretDto:
    def __init__(self, name, fact, key, tags, basepath):
        self.name = name
        self.fact = fact
        self.key = key
        self.tags = tags
        self.basepath = basepath
