import datetime
import json
import uuid


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

    def toJsons(self, secret, key):
        jsons = {
            'header': {
                'name': secret.name,
                'tags': secret.tags,
                'created': secret.created.strftime('%Y-%M-%dT%H:%M:%S.%fZ%z'),
                'algorithm': 'AES256',
                'signature': self.payloadSignatureAlgorithm.sign(secret, key),
                'id': str(secret.id)
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
        self.id = uuid.uuid4()
