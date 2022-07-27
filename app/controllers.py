import app.secret as scrt
import app.secretFileStorage as strge
import fnmatch
import os

def store(secretDto):
    key = secretDto.key
    secret = scrt.Secret(secretDto.name, secretDto.fact, secretDto.tags)
    secretStorage = strge.SecretFileStorage(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()))
    secretStorage.store(secret, key)
    return secret

def readSecret(name, key):
    file = open(name + '.jsons', 'rt')
    return file.read();

def listSecrets():
    secretFiles = list();
    for file in os.listdir('.'):
        print(file)
        if fnmatch.fnmatch(file, '*.jsons'):
            secretFiles.append(file)
    return secretFiles

class SecretDto:
    def __init__(self, name, fact, key, tags):
        self.name = name
        self.fact = fact
        self.key = key
        self.tags = tags

class SecretDaoFactory:
    def __init__(self, dao):
        self.dao = dao

    def getDao(self):
        return self.dao