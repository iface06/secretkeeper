import app.secret as scrt

class SecretFileStorage:
    def __init__(self, jsonsEncryptor):
        self.jsonsEncryptor = jsonsEncryptor

    def store(self, secret, key):
        self.file = open(secret.name + '_' + str(secret.id) +'.jsons', 'wt')
        self.file.write(self.jsonsEncryptor.toJsons(secret, key))
        self.file.close()

    def load(self, name):
        pass
    
    def find(self, name, tags):
        print('SecretFileStorage was called')
