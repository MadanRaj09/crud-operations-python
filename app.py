from flask import Flask, request, jsonify, render_template
import mysql.connector
import os

app = Flask(__name__)

# Establish database connection
database_host = os.environ.get("DATABASE_HOST")
database_user = os.environ.get("DATABASE_USER")
database_password = os.environ.get("DATABASE_PASSWORD")
database_name = os.environ.get("DATABASE_NAME") 

# Use the retrieved environment variables in your code
# For example:
db_config = {
    "host": database_host,
    "user": database_user,
    "password": database_password,
    "database": database_name
}

connection = mysql.connector.connect(**db_config)
cursor = connection.cursor()

# Routes

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read', methods=['GET'])
def read_entries():
    query = "SELECT * FROM users ORDER BY id ASC"
    cursor.execute(query)
    rows = cursor.fetchall()
    data = [{'id': row[0], 'name': row[1], 'age': row[2]} for row in rows]
    return jsonify(data)

@app.route('/create', methods=['POST'])
def create_entry():
    data = request.json
    id = data['id']
    name = data['name']
    age = data['age']
    query = "INSERT INTO users (id,name, age) VALUES (%s,%s,%s)"
    values = (id,name,age)
    cursor.execute(query, values)
    connection.commit()
    return "Record inserted successfully!"

@app.route('/update/<int:user_id>', methods=['PUT'])
def update_entry(user_id):
    data = request.json
    new_age = data['newAge']
    query = "UPDATE users SET age = %s WHERE id = %s"
    values = (new_age, user_id)
    cursor.execute(query, values)
    connection.commit()
    return "Record updated successfully!"

@app.route('/delete/<int:user_id>', methods=['DELETE'])
def delete_entry(user_id):
    query = "DELETE FROM users WHERE id = %s"
    value = (user_id,)
    cursor.execute(query, value)
    connection.commit()
    return "Record deleted successfully!"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)