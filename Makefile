all:
	python setup.py build
	gcc vsh.c -o vsh
