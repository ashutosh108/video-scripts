Installation
============

1. Download python https://www.python.org/downloads/
2. Install python, custom, "add path" or "add environment variables".
3. upgrade pip and setuptools (they are installed by default but newer ones are usually available)
	python -m pip install --upgrade pip
	pip install --upgrade setuptools
4. Install virtualenvwrapper-win
	pip install virtualenvwrapper-win
5. Create new environment
	mkvirtualenv scripts
6. Activate new environment
	workon scripts
7. Install requirements
	(from scripts' source directory)
	pip install -r requirements.txt
That's it!
