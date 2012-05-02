.PHONY: clean dist

dist:
	python setup.py sdist bdist_egg

upload: dist
	python setup.py sdist bdist_egg upload

clean:
	-rm -rf $(BUILDDIR)
	-rm -rf dist
	-rm -rf build
	-rm -rf *.egg-info
	-rm -rf `find . -name *.pyc`