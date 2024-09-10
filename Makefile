flake8:
	flake8 .

test:
	python3 ./tests.py

release:
	python3 setup.py sdist
	twine upload --skip-existing dist/*
