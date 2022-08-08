import app.secret as scrt
import fnmatch
import os
import datetime
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
        secretFiles = self.listSecretFilesSortedByModifiedDate(name)
        if(len(secretFiles) <= 0):
            raise SecretFileNotFound()
        return secretFiles[0]

    def listSecretFilesSortedByModifiedDate(self, name):
        secretFiles = []
        for file in self.secretFilesFromBasePath():
            if fnmatch.fnmatch(file, '*.jsons') and file.startswith(name):
                modifiedDate = self.getModifiedDateFrom(file)
                secretFiles.append(SecretFile(file, modifiedDate))
        secretFiles.sort(key=lambda sf: sf.modifiedDate, reverse=True)
        return secretFiles

    def getModifiedDateFrom(self, file):
        modifiedDate = os.path.getmtime(file)
        return datetime.datetime.fromtimestamp(modifiedDate)

    def find(self, name, tags):
        secretFiles = []
        for file in self.secretFilesFromBasePath():
            if fnmatch.fnmatch(file, '*.jsons') and file.startswith(name):
                modifiedDate = os.path.getmtime(file)
                modifiedDate = datetime.datetime.fromtimestamp(modifiedDate)
                secretFiles.append(SecretFile(file, modifiedDate))
        secretFiles.sort(key=lambda sf: sf.modifiedDate)

        return secretFiles[0]

    def list(self):
        secretFiles = [];
        for file in self.secretFilesFromBasePath():
            if fnmatch.fnmatch(file, '*.jsons'):
                secretFiles.append(SecretFile(file))
        return secretFiles

    def secretFilesFromBasePath(self):
        return os.listdir('.')

class SecretFile:
    def __init__(self, file, modifiedDate=datetime.datetime.now()):
        self.filename = file
        self.modifiedDate = modifiedDate

    def getSecretName(self):
        if(self.filename):
            return self.filename.split('.')[0].split('_')[0]
        else:
            return ''

    def read(self,):
        return open(self.filename, 'rt').read()

class SecretFileNotFound(Exception):
    pass