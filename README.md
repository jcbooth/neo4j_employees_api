== Neo4j Employees API

The following is a simple api implementation is Python using Flask and the Neo4j bolt Python driver to provide a means to write an employee name and ID via a Restful API to be persisted in a Neo4j database instance and all employees returned.

Assumptions are that the default Neo4j database is installed locally with the out-of-the-box neo4j user and password, as well as Python3 installed with pip. 

=== Setup

After pulling the code project down to the local environment, startup a Python virtualenv to run the api:

----
python3 -m venv env
source env/bin/activate
----

Next, install the necessary dependencies:

----
python3 -m pip install flask
python3 -m pip install neo4j
----

Lastly, run the api, as follows:

----
python3 api.py
----

=== API Usage

To add an employee via the api, run the following curl command - the first parameter is for the employee name, and the second for the employee ID:

----
curl -X POST http://127.0.0.1:5000/employees/Jason%20Booth/22
----

To retrieve the employees in the database, run this command (NOTE: currently limited to 25 results. TODO: future features would be to add a parameter for limit and create pagination):

----
curl -X GET http://127.0.0.1:5000/employees
----
 
