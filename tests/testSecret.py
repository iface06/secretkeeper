import unittest
import app.secret as scrt
import json

class TestSecretMethodes(unittest.TestCase):

    def testJsonsStructure(self):
        jsonsEncryptor = scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm())
        jsons, key = jsonsEncryptor.toJsons(scrt.Secret('name', 'fact', ['test1', 'test2']), 'C9fy622ZWqfAY5eWMG1b8/jgOfh1yaFmDGdK9EDxkVY=')
        jsonObj = json.loads(jsons)
        self.assertListEqual(list(jsonObj.keys()), ['header', 'fact'])
        self.assertListEqual(list(jsonObj['header'].keys()), ['name', 'tags', 'created', 'encryptionAlgorithm', 'signature', 'signatureAlgorithm', 'id'])
        self.assertTrue(key)

    def testGenerateKey(self):
        key = scrt.FactEncryptionAlgorithm().generateKey()
        print(len(key))
        self.assertTrue(len(key) >= 24) #Entspricht 128 byte key base64/utf-8 codiert
        self.assertTrue(len(key) < 44) #256 Byte Key soll nicht verwendet werden, weil theoretisch unsicherer

    def testFactEncryption(self):
        ea = scrt.FactEncryptionAlgorithm()
        secret = scrt.Secret('name', 'fact', ['test1', 'test2'])
        key = ea.generateKey();
        encryptedFact = ea.encrypt(secret.fact, key)
        print('Key: ' + key)
        print('Json: ' + encryptedFact)
        self.assertNotEqual(secret.fact, encryptedFact)

    def testSecretDecryption(self):
        key = 'rE4ipl34HRpLVdJ3mWYlrw=='
        jsons = '{"header": {"name": "testee", "tags": ["tag1", "tag2"], "created": "2022-54-01T16:54:45.783304Z", "encryptionAlgorithm": "AES256", "signature": -7020505222687272052, "signatureAlgorithm": "pytonHash", "id": "d31a3750-5044-4f9a-9a90-01d2cbf1667f"}, "fact": "eyJub25jZSI6ICI2cFF4R3RPcnZYUFJqbER1Q0lub1Z3PT0iLCAiY2lwaGVydGV4dCI6ICJucENXc3c9PSIsICJ0YWciOiAiSHVBV1lYYis1Y1ovYmRTMGxYWm5sUT09In0="}'
        decryptor = scrt.JsonsDecryptor(scrt.FactDecryptionAlgorithm())
        secret = decryptor.toSecret(jsons, key)
        self.assertEqual('fact', secret.fact)

if __name__ == '__main__':
    unittest.main()
