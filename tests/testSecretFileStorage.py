import unittest
import app.secret as scrt
import app.secretFileStorage as strg

class TestSecretFileStorage(unittest.TestCase):

    def testSecretFile_splittingFileNameIntoSecretName(self):
        secretName = strg.SecretFile('testapp_uuid.jsons').getSecretName()
        self.assertEqual('testapp', secretName, 'Secret Name extracted from Filename')

    def testList(self):
        secretFiles = SecretFileStorageMock().list()
        self.assertEqual(len(secretFiles), 1)
        self.assertEqual(secretFiles[0].getSecretName(), 'testapp')

    def testFileNameCreation(self):
        filename = SecretFileStorageMock().createSecretFileName(scrt.Secret('testname', 'fact233', []))
        self.assertTrue(filename.startswith('testname_'))
        self.assertTrue(filename.endswith('.jsons'))

class SecretFileStorageMock(strg.SecretFileStorage):
    def __init__(self):
        super().__init__(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.')

    def secretFilesFromBasePath(self):
        return ['testapp_uuid4.jsons']

if __name__ == '__main__':
    unittest.main()