import math


# LocalMemoryDHT implements a DHT stored in the memory in a single machine. The
# DHT contains a list of hash values and their occurrences in the format:
# <hashValue:occurrences>.
class LocalMemoryDHT:
    # hashSize is in bits, and numOfHT is the number of hath tables to use in the
    # distributed hash table.
    def __init__(self, hashSize, numOfHT):
        self.__hashSize = hashSize
        self.__numOfHT = numOfHT

        # Calculate the hash table size.
        size = math.pow(2, hashSize) / numOfHT
        self.__htSize = int(size)
        if int(size) != size:
            self.__numOfHT = self.__numOfHT + 1
            print "Adjusting number of hash tables to " + str(self.__numOfHT)
        # Initializing the hash tables list.
        self.__hashtables = []
        for i in range(0, self.__numOfHT):
            self.__hashtables.append({})


    # insert adds a new hashValue into the DHT. hashValue is an integer or a long
    # integer. If hashValue already exists its occurrence counter is increased.
    def insert(self, hashValue):
        # Calculate the HT ID of this hashValue.
        htId = self._calculateHTId(hashValue)

        # Read the counter of the hash value.
        counter = self.read(hashValue)

        # Increase the occurrence counter for the given hashValue.
        self.__hashtables[htId][hashValue] = counter + 1


    # read reads the number of occurrences of a given hashValue.
    def read(self, hashValue):
        # Calculate the HT ID of this hash value.
        htId = self._calculateHTId(hashValue)

        counter = 0
        if hashValue in self.__hashtables[htId]:
            counter = self.__hashtables[htId][hashValue]
    
        return counter


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
