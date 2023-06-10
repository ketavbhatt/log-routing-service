from flask import Flask, request
import tempfile
import json
import psycopg2
import os

app = Flask(__name__)

# Configuration
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DATABASE_NAME = "mydb"
DATABASE_USER = "myuser"
DATABASE_PASSWORD = "mypassword"


@app.route("/write_temp_file", methods=["POST"])
def write_temp_file():
    data = request.json
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(json.dumps(data).encode())

    return {"message": "Data written to temporary file.", "file_path": temp_file.name}


@app.route("/write_to_database", methods=["POST"])
def write_to_database():
    file_path = request.json.get("file_path")
    if not file_path:
        return {"message": "File path not provided."}, 400

    with open(file_path, "r") as file:
        log_data = file.read()

    # Connect to the database
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD
    )

    # Execute SQL query to insert log data
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (log_data) VALUES (%s)", (log_data,))
    conn.commit()

    # Close database connection
    cursor.close()
    conn.close()

    # Delete the temporary file
    os.remove(file_path)

    return {"message": "Data written to database and temporary file deleted."}

if __name__ == "__main__":
    app.run()
