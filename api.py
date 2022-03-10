import flask
from neo4j import GraphDatabase
from flask import request, jsonify, Response
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def get_driver():
  uri = "bolt://localhost:7687"
  return GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_employee(tx, args):
  name = args["name"]
  emp_id = args["emp_id"]
  result = tx.run("CREATE (e:Employee {name: $name, emp_id: $emp_id})",
             name=name, emp_id=emp_id)

def get_employees(tx, args):
  results = list(tx.run("MATCH (e:Employee) RETURN e.name AS name, e.emp_id AS emp_id LIMIT 25"))
  employees = []
  for record in results:
    employees.append({"name": record["name"], "emp_id": record["emp_id"]})
  return employees

def add_employee_by_id(args):
  return run_neo_tx("create_employee", "write", args)

def get_the_employees(args):
  return run_neo_tx("get_employees", "read", args)

def run_neo_tx(method_name, tx_type, args):
  driver = get_driver()
  with driver.session() as session:
    if tx_type == "write":
      return session.write_transaction(eval(method_name), args)
    elif tx_type == "read":
      return session.read_transaction(eval(method_name), args)
  driver.close()

@app.route("/employees", methods=["GET"])
def get_all_employees():
  args = {"arg": None}
  employees = get_the_employees(args)
  return jsonify(employees)

@app.route("/employees/<name>/<emp_id>", methods=["POST"])
def add_employee(name, emp_id):
  add_employee_by_id({"name": name, "emp_id": emp_id})
  return f"Added employee: {name}, id: {emp_id}"

if __name__ == "__main__":
  app.run()
