Developer Quickstart
====================

Setup development Environment
.............................

.. include:: ../tutorials/installation_content.rst

Testing
.......

Testing framework for nirikshak includes unit tests, functional test cases
and docs checks etc

Unit Test
---------

For unit testing tox has been used, tox includes many testing enviornment

#. py27
#. py35
#. cover
#. pep8
#. docs

All fo the enviornment has different purpose and all of them needs not be
tested before commitng the code

**py27, py35** runs unit tests against  python2.7 and python 3.5. **coverage**
has to be checked for finding the coverage of the unit tests. So if you have
added new code and new branch in the code has been introduced then unit test
for the same has to be written.

**pep8** is used to check the coding standard, if coding standard are not
followed then pep8 will raise the alarm until you don't fix the code
standard. Currently flake is used but plan is to introduce pylint to find
problems at early stage of the testing.

**functional** test cases should be run before submitting any code and any
failure needs to be fixed before submitting. **docs** is used to create
documents for the nirikshak. Documents will be produced in the projects
bulid/html directory and can be acccessed by double clicking on the index.html
file.

Running test cases

.. code::

  tox -e<testing type>

  <testing type> - it can be py27, py35, pep8, docs, cover
                   functional framework has not been introduced yet.

For exmaple, if coding guidlines has to be checked then you should run
following command

.. code::

  tox -epep8

For executing coverage run following commands

.. code::

  tox -cover

For the remaining items, you can use them in the similar way.
