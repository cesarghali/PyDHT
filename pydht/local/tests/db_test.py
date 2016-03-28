import unittest
import shutil

from collections import namedtuple

from pydht.local.db import LocalDbDHT

class LocalDbDHTTest(unittest.TestCase):
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
    __path = "db_dht_tmp"
    __syncLimit = 1


    def __insert(self, distributedHT):
        for case in self.__cases:
            distributedHT.insert(case.hashValue)


    def __cleanup(self):
        # Cleaning up.
        shutil.rmtree(self.__path, ignore_errors=True)


    def test_insert(self):
        distributedHT = LocalDbDHT(8, 10, self.__path,
                                   syncLimit=self.__syncLimit)
        self.__insert(distributedHT)

        distributedHT.close()
        self.__cleanup()


    def test_calculateHTId(self):
        distributedHT = LocalDbDHT(8, 10, self.__path,
                                   syncLimit=self.__syncLimit)

        for case in self.__cases:
            self.assertEqual(distributedHT._calculateHTId(
                case.hashValue), case.htId)

        distributedHT.close()
        self.__cleanup()


    def test_read(self):
        distributedHT = LocalDbDHT(8, 10, self.__path,
                                   syncLimit=self.__syncLimit)
        
        for case in self.__cases:
            distributedHT.insert(case.hashValue)        
            self.assertEqual(distributedHT.read(case.hashValue), case.counter)

        distributedHT.close()
        self.__cleanup()


    def test_calculateCollision(self):
        distributedHT = LocalDbDHT(8, 10, self.__path,
                                   syncLimit=self.__syncLimit)
        self.__insert(distributedHT)

        expected_collision = 4 / 9.0
        self.assertEqual(distributedHT.calculateCollision(), expected_collision)

        distributedHT.close()
        self.__cleanup()


if __name__ == '__main__':
    unittest.main()
