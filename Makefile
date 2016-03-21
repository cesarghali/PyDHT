test:
	python pydht/local/tests/disk_test.py

clean:
	rm -f $(shell find . -name '*.pyc' -type f)
