from flask import Flask, jsonify
import psycopg2
import redis
import time

app = Flask(__name__)

# Connexion à PostgreSQL
pg_conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="postgres",
    dbname="postgres"
)
pg_cursor = pg_conn.cursor()

# Connexion à Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)

@app.route('/query_postgres', methods=['GET'])
def query_postgres():
    start_time = time.time()
    pg_cursor.execute("SELECT * FROM taux_de_change;")
    rows = pg_cursor.fetchall()
    end_time = time.time()
    response_time = end_time - start_time
    return jsonify({
        "source": "PostgreSQL",
        "response_time": response_time,
        "data": rows
    })

@app.route('/query_redis', methods=['GET'])
def query_redis():
    start_time = time.time()
    keys = redis_client.keys("taux_de_change:*")
    rows = [redis_client.hgetall(key) for key in keys]
    end_time = time.time()
    response_time = end_time - start_time
    return jsonify({
        "source": "Redis",
        "response_time": response_time,
        "data": rows
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)