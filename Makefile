MODULES=inquirer

all: pep8 flakes test

test:: run_tests

analysis:: pep8 flakes

coveralls::
	coveralls

run_tests:
	@echo Running Tests...
	@nosetests -d --exe --with-xcoverage --cover-package=${MODULES} --cover-tests

pep8:
	@pep8 --statistics ${MODULES}

flakes:
	@pyflakes ${MODULES}
