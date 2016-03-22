import unittest
import os
import shutil

from collections import namedtuple

from pydht.local.memory import LocalMemoryDHT

class LocalMemoryDHTTest(unittest.TestCase):
    def test_insert(self):
        distributedHT = LocalMemoryDHT(8, 10)

        Case = namedtuple("Case", "hashValue htId counter")
        cases = [
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

        for case in cases:
            self.assertEqual(distributedHT._calculateHTId(
                case.hashValue), case.htId)
            distributedHT.insert(case.hashValue)
            self.assertEqual(distributedHT._read(case.hashValue), case.counter)


    def test_calculateCollision(self):
        distributedHT = LocalMemoryDHT(8, 10)

        Case = namedtuple("Case", "hashValue")
        cases = [
            Case(5),
            Case(10),
            Case(5),
            Case(45),
            Case(100),
            Case(110),
            Case(105),
            Case(110),
            Case(245),
            Case(252)
        ]
        expected_collision = 0.4

        for case in cases:
            distributedHT.insert(case.hashValue)

        self.assertEqual(distributedHT.calculateCollision(), expected_collision)


if __name__ == '__main__':
    unittest.main()
