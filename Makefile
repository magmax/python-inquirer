MODULES=inquirer

all: pep8 flakes test

test:: run_unit_tests run_acceptance_tests

unit_test:: run_unit_tests

acceptance_test:: run_acceptance_tests

analysis:: pep8 flakes

pep8:
	@pep8 --statistics ${MODULES}

flakes:
	@pyflakes ${MODULES}

coveralls::
	coveralls

run_unit_tests:
	@echo Running Tests...
	@nosetests -d --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/unit

run_acceptance_tests:
	@echo Running Tests...
	@nosetests -d --exe --with-xcoverage --cover-package=${MODULES} --cover-tests tests/acceptance
