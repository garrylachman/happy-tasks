pipenv_update:
	pipenv update

pipenv_lock:
	pipenv lock

pipenv_install_local:
	pipenv install --dev -e .

test:
	python setup.py test
