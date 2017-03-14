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


Notes
=====

livestreamer can be used to record livestream.com broadacasts
http://docs.livestreamer.io

1. Get the m3u8 url (from the source of event page)
2. livestreamer "hlsvariant://https://api.new.livestream.com/accounts/2645002/events/7133455/broadcasts/151747450.secure.m3u8?dw=100&hdnea=st=1489495233~exp=1489497033~acl=/i/2645002_7133455_lsitfhycqhbo66gkjj1_1@447492/*~hmac=282c814cf4f259645f45f49bc8440d7df9f994dcf9bb34214ef36b8f1d6c4bfb" best -o "2017-03-14 goswamimj-livestreamer.ts"
