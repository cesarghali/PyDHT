import unittest
import os
import shutil

from collections import namedtuple

from pydht.local.disk import LocalDiskDHT

class LocalDiskDHTTest(unittest.TestCase):
    Case = namedtuple("Case", "hashValue htId counter")
    __cases = [
        Case(5, 0, 1),
        Case(10, 0, 1),
        Case(5, 0, 2),
        Case(45, 1, 1),
        Case(110, 4, 1),
        Case(105, 4, 1),
        Case(110, 4, 2),
        Case(245, 9, 1),
        Case(252, 10, 1)
    ]
    __path = "dht_tmp"


    def __insert(self, distributedHT):
        for case in self.__cases:
            distributedHT.insert(case.hashValue)


    def __cleanup(self):
        # Cleaning up.
        shutil.rmtree(self.__path, ignore_errors=True)


    # This function ensures that a hashValue is stored in htId and it is unique.
    def __ensureUniquness(self, hashValue, htId):
        fileName = os.path.join(self.__path, str(htId))
        occurrence = 0
        with open(fileName, "r") as htFile:
            for line in htFile:
                lineChunks = line.split(":")
                if lineChunks[0] == str(hashValue):
                    occurrence = occurrence + 1

        return (occurrence == 1)


    def test_insert(self):
        distributedHT = LocalDiskDHT(8, 10, self.__path)
        self.__insert(distributedHT)

        for case in self.__cases:
            self.assertTrue(self.__ensureUniquness(case.hashValue, case.htId))

        self.__cleanup()


    def test_calculateHTId(self):
        distributedHT = LocalDiskDHT(8, 10, self.__path)

        for case in self.__cases:
            self.assertEqual(distributedHT._calculateHTId(
                case.hashValue), case.htId)

        self.__cleanup()


    def test_read(self):
        distributedHT = LocalDiskDHT(8, 10, self.__path)
        
        for case in self.__cases:
            distributedHT.insert(case.hashValue)        
            self.assertEqual(distributedHT._read(case.hashValue), case.counter)

        self.__cleanup()


    def test_calculateCollision(self):
        distributedHT = LocalDiskDHT(8, 10, self.__path)
        self.__insert(distributedHT)

        expected_collision = 4 / 9.0
        self.assertEqual(distributedHT.calculateCollision(), expected_collision)

        self.__cleanup()


if __name__ == '__main__':
    unittest.main()
