from flask import Flask, jsonify
import mariadb 


app = Flask(__name__)

# TESTING CONFIG
db_config = {
        "user": "boochi", 
        "password": "",  # HIDE OR OBFUSCATE LATER
        "host": "localhost", 
        "port": 3306,
        "database": "boochi"
        }


def connect_db():
    try:
        connection = mariadb.connect(**db_config)
        return connection

    except mariadb.Error as e:
        print(f"Error connectioning to MariaDB: {e}")
        return None


@app.route("/users", methods=["GET"])
def get_users():
    connection = connect_db()

    if connection is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT id, name, email FROM Users")

        users = []
        for id, name, email in cursor.fetchall():
            user = { 
                "id": id, 
                "name": name, 
                "email": email 
            }
            users.append(user)

        return jsonify(users)

    except mariadb.Error as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "DB query failed"}), 500

    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug = True)

