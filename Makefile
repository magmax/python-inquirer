MODULES=inquirer

all: pep8 flakes test

test:: clear_coverage run_unit_tests run_integration_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: pep8 flakes

pep8:
	@echo Checking PEP8 style...
	@pep8 --statistics ${MODULES} tests

flakes:
	@echo Searching for static errors...
	@pyflakes ${MODULES}

coveralls::
	coveralls

run_unit_tests:
	@echo Running Tests...
	@nosetests -d --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/unit

run_integration_tests:
	@echo Running Tests...
	@nosetests -d --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/integration

run_acceptance_tests:
	@echo Running Tests...
	@nosetests -d --exe tests/acceptance

clear_coverage:
	@echo Cleaning previous coverage...
	@coverage erase