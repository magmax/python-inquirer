all: flakes test

test:: clear_coverage run_integration_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: flakes

flakes:
	@echo Searching for static errors...
	@flake8 --statistics --count  inquirer tests

coveralls::
	coveralls

publish::
	@python setup.py sdist bdist_wheel upload

run_unit_tests:
	@echo Running Tests...
	@py.test --cov inquirer --cov-report=term-missing --no-cov-on-fail tests/unit

run_integration_tests:
	@echo Running Tests...
	@py.test --cov inquirer --cov-report=term-missing --no-cov-on-fail tests/unit tests/integration

run_acceptance_tests:
	@echo Running Tests...
	@py.test tests/acceptance

clear_coverage:
	@echo Cleaning previous coverage...
	@coverage erase
