from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
import json
import requests

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "123"
app.config["MYSQL_DB"] = "data_flask"

mysql = MySQL(app)


@app.route("/")
def index():
    return "!HOLA MUNDO!!"


# READ
@app.route("/usuarios")
def obtenerUsuarios():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    return jsonify(usuarios)


# CREATE
@app.route("/crear", methods=["POST"])
def crearUsuario():
    datos = request.json
    nombre = datos["nombre"]
    correo = datos["correo"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, correo) VALUES (%s, %s)", (nombre, correo)
    )
    # cursor.execute(f"INSERT INTO usuarios (nombre, correo) VALUES ('{nombre}','{correo}')")
    mysql.connection.commit()
    cursor.close()
    return "Usuario agregado!"


# UPDATE
@app.route("/update/<int:id>", methods=["PUT"])
def editarUsuario(id):
    datos = request.json
    nombre = datos["nombre"]
    correo = datos["correo"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre = %s, correo = %s WHERE id = %s",
        (nombre, correo, id),
    )
    mysql.connection.commit()
    cursor.close()
    return "Usuario Actualizado"


# DELETE


@app.route("/eliminar_usuario/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
    mysql.connection.commit()
    cursor.close()
    return "Usuario ELIMINADO", 200


@app.route("/guardar", methods=["POST"])
def guardar():
    datos = request.json
    print(datos)
    with open("./archivo.json", "w") as json_file:
        json.dump(datos, json_file)
    return "informacion leida"


@app.route("/guardar_text", methods=["POST"])
def guardar_text():
    data = request.form.get("text")
    print(data)
    with open("./archivo.txt", "w") as texto:
        texto.write(data)
    return "Texto Guardado"


@app.route("/leer_json")
def leer_json():
    with open("./archivo.json", "r") as jsonFile:
        data = [json.load(jsonFile)]
        print(data)
    return "JSON leido"


@app.route("/leer_text")
def leer_text():
    with open("./archivo.txt", "r") as textFile:
        contenido = textFile.read()
        print(contenido)
    return "Texto Leido"


@app.route("/placeholder")
def placeholder():
    # URL de la API de jsonplaceholder
    url = "https://jsonplaceholder.typicode.com/users"

    # Realizar la solicitud GET a jsonplaceholder
    response = requests.get(url)


if __name__ == "__main__":
    app.run(debug=True)

# host "localhost"
# DB: data_flask
# user: root
# pass: 123

# MySQLdb.cursors.DictCursor
# pip install flask-mysqldb
