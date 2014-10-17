MODULES=inquirer

all: flakes test

test:: clear_coverage run_unit_tests run_integration_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: flakes

flakes:
	@echo Searching for static errors...
	@flake8 --statistics --count  ${MODULES} tests

coveralls::
	coveralls

publish: run_publish run_tag

run_publish::
	@python setup.py sdist bdist_wheel upload

run_tag::
	@python -m releaseme --git --file releaseme/__init__.py

run_unit_tests:
	@echo Running Tests...
	@nosetests -dv --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/unit

run_integration_tests:
	@echo Running Tests...
	@nosetests -dv --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/integration

run_acceptance_tests:
	@echo Running Tests...
	@nosetests -dv --exe tests/acceptance

clear_coverage:
	@echo Cleaning previous coverage...
	@coverage erase
