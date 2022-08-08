import datetime
import os.path
import unittest
import app.secret as scrt
import app.secretFileStorage as strg

class TestSecretFileStorage(unittest.TestCase):

    def testSecretFile_splittingFileNameIntoSecretName(self):
        secretName = strg.SecretFile('testapp_uuid.jsons').getSecretName()
        self.assertEqual('testapp', secretName, 'Secret Name extracted from Filename')

    def testList(self):
        secretFiles = SecretFileStorageMock().list()
        self.assertEqual(len(secretFiles), 3)
        self.assertEqual(secretFiles[0].getSecretName(), 'testapp')

    def testFileNameCreation(self):
        filename = SecretFileStorageMock().createSecretFileName(scrt.Secret('testname', 'fact233', []))
        self.assertTrue(filename.startswith('testname_'))
        self.assertTrue(filename.endswith('.jsons'))

    def testFindSecretFileByName(self):
        jsonsFile = SecretFileStorageMock().load('testfile')
        self.assertEqual('testfile_uuid41.jsons', jsonsFile.filename)

    def testDoNotFindSecreteFileByName(self):
        load = lambda: SecretFileStorageMock().load('notafile')
        self.assertRaises(strg.SecretFileNotFound, load)


class SecretFileStorageMock(strg.SecretFileStorage):
    def __init__(self):
        super().__init__(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.')

    def secretFilesFromBasePath(self):
        return ['testapp_uuid4.jsons', 'testfile_uuid42.jsons', 'testfile_uuid41.jsons']

    def getModifiedDateFrom(self, file):
        return datetime.datetime.now()

if __name__ == '__main__':
    unittest.main()