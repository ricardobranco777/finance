FILES=*.py

.PHONY: testall
testall: flake8 pylint mypy black

.PHONY: flake8
flake8:
	@flake8 --ignore=E501 $(FILES)

.PHONY: pylint
pylint:
	@pylint --disable=line-too-long $(FILES)

.PHONY: mypy
mypy:
	@mypy $(FILES)

.PHONY: black
black:
	@black --check $(FILES)
