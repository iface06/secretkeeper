import app.secret as scrt
import fnmatch
import os

class SecretFileStorage:
    def __init__(self, jsonsEncryptor, basePath = '.'):
        self.jsonsEncryptor = jsonsEncryptor
        self.basePath = basePath

    def store(self, secret, key):
        print(self.createSecretFileName(secret))
        self.file = open(self.createSecretFileName(secret), 'wt')
        json, key = self.jsonsEncryptor.toJsons(secret, key)
        self.file.write(json)
        self.file.close()
        return key

    def createSecretFileName(self, secret):
        return secret.name + '_' + str(secret.id) +'.jsons'

    def load(self, name):
        pass

    def find(self, name, tags):
        print('SecretFileStorage was called')

    def list(self):
        secretFiles = [];
        for file in self.secretFilesFromBasePath():
            if fnmatch.fnmatch(file, '*.jsons'):
                secretFiles.append(SecretFile(file))
        return secretFiles

    def secretFilesFromBasePath(self):
        return os.listdir('.')

class SecretFile:
    def __init__(self, file):
        self.filename = file

    def getSecretName(self):
        if(self.filename):
            return self.filename.split('.')[0].split('_')[0]
        else:
            return ''