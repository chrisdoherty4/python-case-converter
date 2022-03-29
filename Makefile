PYTHON := python3

test:
	$(PYTHON) -m pytest ./caseconverter/

package:
	$(PYTHON) -m build

check:
	$(PYTHON) -m twine check dist/*

upload:
	$(PYTHON) -m twine upload dist/*