"""
2024-12-05
ADDED: get_users, add_users, get_events
TODO: unfortunately need to HEAVILY reanalyze schema and redesign
      -- constraints, checks, normalization, foreign key constraints, ...
      -- i do not think it will have too much of an impact on Events table
"""

from datetime import datetime, time
from flask import Flask, request, jsonify

from mariadb_pw import get_mariadb_test_pw
import mariadb 


app = Flask(__name__)

# TESTING CONFIG
db_config = {
        "user": "boochi", 
        "password": get_mariadb_test_pw(),         "host": "localhost", 
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


# -------- Users --------

@app.route("/users", methods=["GET"])
def get_users():
    connection = connect_db()

    if connection is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = connection.cursor()
    try:
        # excluding Users.password
        cursor.execute("SELECT user_id, username, email, first_name, last_name, signup_date, paid_dues FROM Users")

        users = []
        for user_id, username, email, first_name, last_name, signup_date, paid_dues in cursor.fetchall():
            user = { 
                    "user_id": user_id, 
                    "username": username, 
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "signup_date": signup_date,  # time zone in db is GMT, need to change
                    "paid_dues": paid_dues
                    }
            users.append(user)

        return jsonify(users)

    except mariadb.Error as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "DB query failed"}), 500

    finally:
        cursor.close()
        connection.close()


# for now using `curl .....` to test
@app.route("/users", methods=["POST"])
def add_users():
    data = request.json
    
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    signup_date = data.get("signup_date")
    paid_dues = data.get("paid_dues")

    # ---- test for valid post, implement later assume good input ----
    # e.g. if not email or.... return jsonify({"error": "missing"})

    connection = connect_db()

    if connection is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, email, password, first_name, last_name, signup_date, paid_dues) VALUES (?, ?, ?, ?, ?, ?, ?)", (username, email, password, first_name, last_name, signup_date, paid_dues))
        connection.commit()

        # user_id is AUTO_INCREMENT even on failed insert into queries.
        # it is not an issue. the main purpose is uniqueness as a PK.
        return jsonify({"message": "User added successfully", "user_id": cursor.lastrowid}), 201

    except mariadb.Error as e:
        print(f"Error inserting data to database: {e}")
        return jsonify({"error": "DB insertion failed"}), 500

    finally:
        cursor.close()
        connection.close()

# -------- Events --------

@app.route("/events", methods=["GET"])
def get_events():
    connection = connect_db()

    if connection is None:
        return jsonify({"error": "Failed to connect to database"}), 500

    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM Events")

        events = []
        for event_id, title, desc, loc, date_time, end_time in cursor.fetchall():

            event = {
                    "event_id": event_id,
                    "title": title,
                    "description": desc,
                    "location": loc,
                    "datetime": date_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end_time": end_time.strftime("%Y-%m-%dT%H:%M:%S")
                    }

            events.append(event)

        return jsonify(events)

    except mariadb.Error as e:
        print(f"Error fetching data: {e}")
        return jsonify({"error": "DB query failed"}), 500

    finally:
        cursor.close()
        connection.close()


# @app.route("/events", methods=["POST"])
# def add_events():


if __name__ == '__main__':
    app.run(debug = True)
