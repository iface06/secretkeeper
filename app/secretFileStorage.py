import app.secret as scrt
import fnmatch
import os
import datetime
import json

class SecretFileStorage:
    def __init__(self, jsonsEncryptor, basePath = '.'):
        self.jsonsEncryptor = jsonsEncryptor
        self.basePath = basePath

    #ToDo MoveJsonEncryptor to Controllers.store
    #ToDo open() with basePath
    #ToDo One Secret File vs. Secret and Fact-File (large Facts)
    def store(self, secret, key):
        self.file = open(self.createSecretFileNameWithBasePath(secret), 'wt')
        json, key = self.jsonsEncryptor.toJsons(secret, key)
        self.file.write(json)
        self.file.close()
        return key

    def createSecretFileName(self, secret):
        return secret.name + '_' + str(secret.id) +'.jsons'

    def createSecretFileNameWithBasePath(self, secret):
        filename = self.createSecretFileName(secret)
        return os.path.join(self.basePath, filename)

    def load(self, name):
        secretFiles = self.listSecretFilesSortedByModifiedDate(name)
        if(len(secretFiles) <= 0):
            raise SecretFileNotFound()
        return self.readJsonsFromFile(secretFiles[0].filename)

    def listSecretFilesSortedByModifiedDate(self, name):
        secretFiles = []
        for file in self.secretFilesFromBasePath():
            if fnmatch.fnmatch(file, '*.jsons') and file.startswith(name):
                jsons = self.readJsonsFromFile(file)
                secretFiles.append(SecretFile(file, jsons['header']['created'], jsons['header']['tags']))
        secretFiles.sort(key=lambda sf: sf.modifiedDate, reverse=True)
        return secretFiles

    def getModifiedDateFrom(self, file):
        modifiedDate = os.path.getmtime(file)
        return datetime.datetime.fromtimestamp(modifiedDate)

    def find(self, tags):
        files = self.secretFilesFromBasePath()
        secretFileNames = self.__distinctFileNameSet(files)
        secretFiles = self.__createSecretFiles(secretFileNames)
        found = []
        for secretFile in secretFiles:
            for tag in tags:
                if tag in secretFile.tags:
                    found.append(secretFile)

        return found

    def readJsonsFromFile(self, secretFile):
        jsonsFileContent = open(secretFile, 'rt').read()
        return json.loads(jsonsFileContent)


    def list(self):
        filesFromHd = self.secretFilesFromBasePath()
        secretFiles = self.__createSecretFiles(filesFromHd)
        secretFiles.sort(key=lambda sf: sf.modifiedDate, reverse=True)
        SecretFileDict = {}
        for secretFile in secretFiles:
            SecretFileDict[secretFile.getSecretName()] = secretFile
        return list(SecretFileDict.values())

    def __distinctFileNameSet(self, filesFromHd):
        secretFiles = set();
        for file in filesFromHd:
            if fnmatch.fnmatch(file, '*.jsons'):
                secretFiles.add(file)
        return secretFiles

    def __createSecretFiles(self, fileNames):
        files = []

        for fileName in fileNames:
            jsons = self.readJsonsFromFile(fileName)
            filetags = jsons['header']['tags']
            secretFile = SecretFile(fileName, jsons['header']['created'], jsons['header']['tags'])
            files.append(secretFile)
        return files

    def secretFilesFromBasePath(self):
        files = os.listdir('.')
        files.sort()
        return files


    def __readFilePerLine(self, filename):
        with open(filename,'r',buffering=1) as f:
            for line in f:
                print(line)

    def __readFileBuffered(self, filename, bufferSizeInByte):
        with open(filename,'r',buffering=bufferSizeInByte) as f:
            for line in f:
                print(line)

class SecretFile:
    def __init__(self, filename, modifiedDate, tags):
        self.filename = filename
        self.modifiedDate = modifiedDate
        self.tags = tags

    def getSecretName(self):
        if(self.filename):
            return self.filename.split('.')[0].split('_')[0]
        else:
            return ''

class SecretFileNotFound(Exception):
    pass