import math
import shelve
import shutil
import os
import os.path


# LocalDbDHT implements a DHT stored in shelve objects in a single machine. The
# DHT contains a list of hash values and their occurrences in the format:
# <hashValue:occurrences>.
class LocalDbDHT:
    # hashSize is in bits, and numOfHT is the number of hath tables to use in the
    # distributed hash table, the directory path where the hash table database
    # files will be stored, and syncLimit contains the number of inserts before
    # the shelve object is being synced.
    def __init__(self, hashSize, numOfHT, path, syncLimit=100):
        self.__hashSize = hashSize
        self.__numOfHT = numOfHT

        # Calculate the hash table size.
        size = math.pow(2, hashSize) / numOfHT
        self.__htSize = int(size)
        if int(size) != size:
            self.__numOfHT = self.__numOfHT + 1
            print "Adjusting number of hash tables to " + str(self.__numOfHT)

        self.__path = path
        self.__createDirectory()

        # Initializing the hash tables list.
        self.__hashtables = []
        self.__syncCounter = []
        for i in range(0, self.__numOfHT):
            fileName = os.path.join(self.__path, str(i))
            self.__hashtables.append(shelve.open(fileName, writeback=True))
            self.__syncCounter.append(0)

        self.__syncLimit = syncLimit


    # Create the hash table directory, first remove it if it exists.
    def __createDirectory(self):
        if os.path.isdir(self.__path):
            shutil.rmtree(self.__path, ignore_errors=True)
        os.makedirs(self.__path)


    # insert adds a new hashValue into the DHT. hashValue is an integer or a long
    # integer. If hashValue already exists its occurrence counter is increased.
    def insert(self, hashValue):
        # Calculate the HT ID of this hashValue.
        htId = self._calculateHTId(hashValue)

        # Read the counter of the hash value.
        counter = self.read(hashValue)

        # Increase the occurrence counter for the given hashValue.
        self.__hashtables[htId][str(hashValue)] = counter + 1
        self.__syncCounter[htId] = (self.__syncCounter[htId] + 1) % \
                                   self.__syncLimit
        if self.__syncCounter[htId] == 0:
            self.__hashtables[htId].sync()


    # read reads the number of occurrences of a given hashValue.
    def read(self, hashValue):
        # Calculate the HT ID of this hash value.
        htId = self._calculateHTId(hashValue)

        counter = 0
        if str(hashValue) in self.__hashtables[htId]:
            counter = self.__hashtables[htId][str(hashValue)]
    
        return counter


    # close closes all shelve instances.
    def close(self):
        for i in range(0, self.__numOfHT):
            self.__hashtables[i].close()


    # _calculateHTId calculates the HT ID of a given hashValue.
    def _calculateHTId(self, hashValue):
        htId = int(hashValue / self.__htSize)
        # This throws and error if htId is larger than number of hash tables.
        assert htId < self.__numOfHT
        return htId


    # calculateCollision calculates the collision probability of this hash table.
    def calculateCollision(self):
        # Total contains the sum of all hash value occurrences in the DHT.
        total = 0
        # Count contains the sum of occurrences of hash values with collision,
        # e.g., occurrence value larger than 1.
        count = 0
        for i in range(0, self.__numOfHT):
            for key in self.__hashtables[i]:
                if self.__hashtables[i][key] > 1:
                    count = count + self.__hashtables[i][key]
                total = total + self.__hashtables[i][key]

        return count / float(total)
