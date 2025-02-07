from flask import Flask, jsonify, request
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from time import sleep
# from opentelemetry.instrumentation.flask import FlaskInstrumentor
# from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor
# from opentelemetry.instrumentation.requests import RequestsInstrumentor



app = Flask(__name__)
# FlaskInstrumentor().instrument_app(app)
# Psycopg2Instrumentor().instrument()
# RequestsInstrumentor().instrument()

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

@app.route('/sql', methods=['GET'])
def execute_query():
    query = 'Select count(*) from faq'

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            if cur.description: 
                results = cur.fetchall()
                return jsonify({"results": results}), 200
            else: 
                conn.commit()
                return jsonify({"message": "Query executed successfully"}), 200
    except psycopg2.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route('/root', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/ping', methods=['GET'])
def curl_google():
    try:
        sleep(4)
        response = requests.get("https://www.google.com")
        sleep(2)
        response = requests.get("https://www.youtube.com")
        sleep(1)
        response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=35&longitude=139&hourly=temperature_2m")
        sleep(3)
        return jsonify(
            status_code=response.status_code,
            content='curl google result'
        )
    except requests.exceptions.RequestException as e:
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    DB_CONFIG = {
    "host": "10.50.16.20",
    "database": "hpipe_dev",
    "user": "hpipe_admin",
    "password": "gemini123",
    "port": 5432
}
    
    app.run(port=5000, host="0.0.0.0")
