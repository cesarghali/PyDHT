test:
	python pydht/local/tests/disk_test.py
	python pydht/local/tests/memory_test.py

clean:
	rm -f $(shell find . -name '*.pyc' -type f)

install:
	python setup.py install
