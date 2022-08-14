import datetime
import json
import os.path
import unittest
import app.secret as scrt
import app.secretFileStorage as strg

class TestSecretFileStorage(unittest.TestCase):

    def testSecretFile_splittingFileNameIntoSecretName(self):
        secretName = strg.SecretFile('testapp_uuid.jsons', datetime.datetime.now(), ['test1']).getSecretName()
        self.assertEqual('testapp', secretName, 'Secret Name extracted from Filename')

    def testList(self):
        secretFiles = SecretFileStorageMock().list()
        self.assertEqual(2, len(secretFiles))
        self.assertEqual('testfile', secretFiles[1].getSecretName())
        self.assertEqual('testapp', secretFiles[0].getSecretName())

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

    def testFindByTag(self):
        tags = ['testapp']
        secrets = SecretFileStorageMock().find(tags)
        self.assertEqual(1, len(secrets))


    def testFindByTag(self):
        tags = ['dev']
        secrets = SecretFileStorageMock().find(tags)
        self.assertEqual(2, len(secrets))
        for secret in secrets:
            self.assertIn('dev', secret.tags)


class SecretFileStorageMock(strg.SecretFileStorage):
    def __init__(self):
        super().__init__(scrt.JsonsEncryptor(scrt.FactEncryptionAlgorithm(), scrt.FactSignatureAlgorithm()), '.')

    def secretFilesFromBasePath(self):
        files = ['testapp_uuid4.jsons', 'testfile_uuid42.jsons', 'testfile_uuid41.jsons']
        return files

    def getModifiedDateFrom(self, file):
        return datetime.datetime.now()

    def readJsonsFromFile(self, secretFile):
        testfiles = {
            'testapp_uuid4.jsons': json.loads('{"header": {"name": "testapp", "tags": ["testapp", "dev"], "created": "2022-26-08T12:26:11.923910Z", "encryptionAlgorithm": "AES256", "signature": 7139622931551893719, "signatureAlgorithm": "pytonHash", "id": "72372dad-7840-4cb8-abbf-f5e8a2ec15b2"}, "fact": "eyJub25jZSI6ICJpZ2lDK3RFZlZiZ0tZa3hoRnh3RStRPT0iLCAiY2lwaGVydGV4dCI6ICJQRnFNMkRxODJ4bUtXR0J4U1R5cTZtMUdTVzExaFUwV056SmRrbjR2a2tqRDB1WT0iLCAidGFnIjogImRzYWxMOW9JNEtxdVpscFpEdUl0ZVE9PSJ9"}'),
            'testfile_uuid41.jsons': json.loads('{"header": {"name": "testfile", "tags": ["testfile", "prod"], "created": "2022-26-08T12:26:11.923910Z", "encryptionAlgorithm": "AES256", "signature": 7139622931551893719, "signatureAlgorithm": "pytonHash", "id": "72372dad-7840-4cb8-abbf-f5e8a2ec15b2"}, "fact": "eyJub25jZSI6ICJpZ2lDK3RFZlZiZ0tZa3hoRnh3RStRPT0iLCAiY2lwaGVydGV4dCI6ICJQRnFNMkRxODJ4bUtXR0J4U1R5cTZtMUdTVzExaFUwV056SmRrbjR2a2tqRDB1WT0iLCAidGFnIjogImRzYWxMOW9JNEtxdVpscFpEdUl0ZVE9PSJ9"}'),
            'testfile_uuid42.jsons': json.loads( '{"header": {"name": "testfile", "tags": ["testfile", "dev"], "created": "2022-01-08T10:30:11.923910Z", "encryptionAlgorithm": "AES256", "signature": 7139622931551893719, "signatureAlgorithm": "pytonHash", "id": "72372dad-7840-4cb8-abbf-f5e8a2ec15b2"}, "fact": "eyJub25jZSI6ICJpZ2lDK3RFZlZiZ0tZa3hoRnh3RStRPT0iLCAiY2lwaGVydGV4dCI6ICJQRnFNMkRxODJ4bUtXR0J4U1R5cTZtMUdTVzExaFUwV056SmRrbjR2a2tqRDB1WT0iLCAidGFnIjogImRzYWxMOW9JNEtxdVpscFpEdUl0ZVE9PSJ9"}')
        }
        return testfiles[secretFile]

if __name__ == '__main__':
    unittest.main()