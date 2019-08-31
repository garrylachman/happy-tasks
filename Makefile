pipenv_update:
	pipenv update

pipenv_lock:
	pipenv lock

pipenv_install_local:
	pipenv install -e .

test:
	python setup.py test