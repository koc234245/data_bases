from flask import Flask, jsonify, request
import psycopg2


app = Flask(__name__)


def create_connection():
    connection = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="26032000"
    )
    return connection


@app.route('/')
def index():
    return "Hello World"


@app.route('/employees', methods=['GET'])
def get_employees():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    employees = []
    for row in rows:
        employee = {
            'id': row[0],
            'name': row[1],
            'surname': row[2],
            'salary': row[3],
            'departament_id': row[4]
        }
        employees.append(employee)
    return jsonify({'employees': employees})


@app.route('/employees', methods=['GET', 'POST'])
def add_employees():
    connection = create_connection()
    cursor = connection.cursor()

    data = request.json
    name = data['name']
    surname = data['surname']
    salary = data['salary']
    departament_id = data['departament_id']

    query = 'INSERT INTO employees ("departament_id", "name", "surname", "salary") VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (departament_id, name, surname, salary))
    connection.commit()

    cursor.close()
    connection.close()

    return "Employee added successfully"



@app.route('/departaments', methods=['GET'])
def get_departments():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="26032000"
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM departaments")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    departaments = []
    for row in rows:
        departament = {
            'id': row[0],
            'name': row[1],
            'location': row[2],
        }
        departaments.append(departament)
    return jsonify({'departaments': departaments})

@app.route('/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    connection = create_connection()
    cursor = connection.cursor()

    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (id,))
    connection.commit()

    cursor.close()
    connection.close()

    return "Employee deleted successfully"


@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    connection = create_connection()
    cursor = connection.cursor()
    data = request.get_json()
    
    name = data.get('name')
    surname = data.get('surname')
    salary = data.get('salary')
    departament_id = data.get('departament_id')
    
    query = 'UPDATE employees SET name = %s, surname = %s, salary = %s, departament_id = %s WHERE id = %s'
    cursor.execute(query, (name, surname, salary, departament_id, id))
    
    connection.commit()
    
    return 'Employee updated successfully'


if __name__ == '__main__':
    app.run()