# PyDHT - Python Distributed Hash Table

[![Build Status](https://travis-ci.org/cesarghali/PyDHT.svg?branch=master)](https://travis-ci.org/cesarghali/PyDHT) [![Coverage Status](https://coveralls.io/repos/github/cesarghali/PyDHT/badge.svg?branch=master)](https://coveralls.io/github/cesarghali/PyDHT?branch=master)

PyDHT is a Python implementation of distributed hashtable stored on a local machine. The implementation supports the DHT being stored in memory, on disk, or in a database. The DHT contains a list of hash values and their number of occurrences.

## Installation

Follow the following steps to install PyDHT on Ubuntu:

```
$ git clone git@github.com:cesarghali/PyDHT.git
$ cd PyDHT
$ make
$ make test
$ sudo make install
```

## Usage

PyDHT provides three flavors of a distributed hashtable stored on a single machine.

### `LocalDiskDHT` Class

This class implements a DHT stored in text files on disk. Each hashtable is stored in a separate text file and includes a list of hash values and their number of occurrences in the format `<hashValue:occurrences>`. This class constructor expects the following parameters:

* `hashSize` -- the size of the hash value in bits.
* `numOfHT` -- the number of hashtables.
* `path` -- the directory path where the hashtables will be stored on disk.

One drawback of this class is that each time the number of occurrences of a specific hash value is increased, the whole corresponding hashtable file is copied.

For a usage example see [`LocalDiskDHTTest`](https://github.com/cesarghali/PyDHT/blob/master/pydht/local/tests/disk_test.py).

### `LocalMemoryDHT` Class

This class implements a DHT stored in memory. Each hashtable is represented as a python dictionary object. The dictionary key is the hash value itself, while the dictionary value is the number of occurrences. This class constructor expects the following parameters:

* `hashSize` -- the size of the hash value in bits.
* `numOfHT` -- the number of hashtables.

For a usage example see [`LocalDiskDHTTest`](https://github.com/cesarghali/PyDHT/blob/master/pydht/local/tests/memory_test.py).

### `LocalDbDHT` Class

This class implements a DHT stored in database on disk. Each hashtable is stored in a separate python [shelve](https://docs.python.org/2/library/shelve.html) object. This class constructor expects the following parameters:

* `hashSize` -- the size of the hash value in bits.
* `numOfHT` -- the number of hashtables.
* `path` -- the directory path where the hashtable database files will be stored.
* `syncLimit` -- is the number of inserts before the corresponding shelve object is being synced.

For a usage example see [`LocalDiskDHTTest`](https://github.com/cesarghali/PyDHT/blob/master/pydht/local/tests/db_test.py).

## APIs

Each of the above three classes provides the following APIs.

* `insert` -- takes a hash value as a positive integer (or long integer) parameter and (1) inserts it in the corresponding hashtable with 1 as its number of occurrences, or (2) increases the number of occurrences by one if the hash value already exists.
* `read` -- takes a hash value as a positive integer (or long integer) parameter and returns its number of occurrences. If the hash value does not exist, 0 is returned.
* `exists` -- takes a hash value as a positive integer (or long integer) parameter and returns `True` if such value exists in the distributed hashtable, or `False` otherwise.
* `calculateCollision` -- calculates the probability of collisions in the current DHT.
* `countCollision` -- counts the hash buckets that have collision, the number of inserted hash values that collide, and the total number of hash values inserted into the DHT.

Additionally, `LocalDbDHT` provides a `close` API that closes all shelve instances.


## License

PyDHT is licensed under the GPLv3: [http://www.gnu.org/licenses/gpl-3.0.html](http://www.gnu.org/licenses/gpl-3.0.html).


## Disclaimer

PyDHT is developed and tested in Ubuntu 14.04 TLS. It **should** theoretically work in other environments.

