from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors

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


if __name__ == "__main__":
    app.run(debug=True)

# host "localhost"
# DB: data_flask
# user: root
# pass: 123

# MySQLdb.cursors.DictCursor
# pip install flask-mysqldb


