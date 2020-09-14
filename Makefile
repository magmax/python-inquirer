all: flakes test

test:: run_integration_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: flakes

doc:
	sphinx-apidoc inquirer -o docs/source -f
	python setup.py build_sphinx

flakes:
	@echo Searching for static errors...
	@flake8 inquirer tests

coveralls::
	coveralls

publish::
	@python setup.py sdist bdist_wheel upload
	@python -m releaseme --git --file inquirer/__init__.py

run_unit_tests::
	@echo Running Tests...
	@py.test tests/unit

run_integration_tests::
	@echo Running Tests...
	@py.test tests/unit tests/integration

run_acceptance_tests::
	@echo Running Tests...
	@py.test tests/acceptance
