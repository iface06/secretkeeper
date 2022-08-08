import unittest
import os
import datetime
import app.secretFileStorage as soae

class FileSystemStaff(unittest.TestCase):

    def testMetaFileLoading(self):
        modifiedTimestamp = os.path.getmtime('testSecret.py')
        modifiedDate = datetime.datetime.fromtimestamp(modifiedTimestamp)
        print('Modified: ' + str(modifiedTimestamp))
        print('Modified: ' + modifiedDate.strftime('%d-%m-%Y %H:%M:%S'))


