from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "movie_db")
    )

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS reservations (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    movie VARCHAR(255)
                )""")
    conn.commit()
    conn.close()

@app.route("/")
def home():
    return "<h1>🎬 Movie Reservation System is Running</h1>"

@app.route('/reservations', methods=['POST'])
def create_reservation():
    data = request.get_json()
    name = data['name']
    movie = data['movie']
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO reservations (name, movie) VALUES (%s, %s)", (name, movie))
    conn.commit()
    conn.close()
    return jsonify({"message": "Reservation created"}), 201

@app.route('/reservations', methods=['GET'])
def list_reservations():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, movie FROM reservations")
    results = c.fetchall()
    conn.close()
    reservations = [{"id": r[0], "name": r[1], "movie": r[2]} for r in results]
    return jsonify(reservations)


@app.route("/movies")
def list_movies():
    return {"movies": ["Inception", "The Matrix", "Interstellar"]}

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8000)