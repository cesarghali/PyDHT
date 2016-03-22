TEST_FILES = $(shell find pydht/local/tests/ -type f \( -iname "*.py" ! -iname "__init__.py" \))

test:
	for t in $(TEST_FILES) ; do \
		python $$t ; \
	done

coverage:
	for t in $(TEST_FILES) ; do \
		coverage run -a --source=pydht $$t ; \
	done

clean:
	rm -f $(shell find . -name '*.pyc' -type f)
	rm -f $(shell find . -name '.coverage' -type f)

install:
	python setup.py install
