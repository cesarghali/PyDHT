import unittest

from collections import namedtuple

from pydht.local.memory import LocalMemoryDHT

class LocalMemoryDHTTest(unittest.TestCase):
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
    __nonExistingCases = [
        Case(55, 0, 0),
        Case(65, 0, 0),
        Case(163, 0, 0)
    ]


    def __insert(self, distributedHT):
        for case in self.__cases:
            distributedHT.insert(case.hashValue)


    def test_insert(self):
        distributedHT = LocalMemoryDHT(8, 10)
        self.__insert(distributedHT)


    def test_calculateHTId(self):
        distributedHT = LocalMemoryDHT(8, 10)

        for case in self.__cases:
            self.assertEqual(distributedHT._calculateHTId(
                case.hashValue), case.htId)


    def test_read(self):
        distributedHT = LocalMemoryDHT(8, 10)
        
        for case in self.__cases:
            distributedHT.insert(case.hashValue)        
            self.assertEqual(distributedHT.read(case.hashValue), case.counter)


    def test_exists(self):
        distributedHT = LocalMemoryDHT(8, 10)
        self.__insert(distributedHT)

        for case in self.__cases:
            self.assertTrue(distributedHT.exists(case.hashValue))

        for case in self.__nonExistingCases:
            self.assertFalse(distributedHT.exists(case.hashValue))


    def test_calculateCollision(self):
        distributedHT = LocalMemoryDHT(8, 10)
        self.__insert(distributedHT)

        expected_collision = 4 / 9.0
        self.assertEqual(distributedHT.calculateCollision(), expected_collision)


    def test_countCollision(self):
        distributedHT = LocalMemoryDHT(8, 10)
        self.__insert(distributedHT)

        expectedHashCount = 2
        expectedValueCount = 4
        expectedTotalCount = 9
        hashCount, valueCount, totalCount = distributedHT.countCollision()
        self.assertEqual(hashCount, expectedHashCount)
        self.assertEqual(valueCount, expectedValueCount)
        self.assertEqual(totalCount, expectedTotalCount)


if __name__ == '__main__':
    unittest.main()
