from flask import Flask, request, jsonify, render_template
import mysql.connector
import re

app = Flask(__name__)

def get_db_connection():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="96522",
            database="transport_db"
        )
        print("Database connection established!")
        return db
    except mysql.connector.Error as err:
        print(f"Database connection failed: {err}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_transport():
    db = None
    cursor = None
    try:
        data = request.get_json()
        if not data or "query" not in data:
            print("Invalid JSON data received")
            return jsonify({"error": "Invalid JSON data received"}), 400
        
        query = data.get("query", "").lower()
        print(f"Received query: {query}")

        if not query:
            print("Empty query received")
            return jsonify({"error": "No query received"}), 400

        # Use regex to extract source and destination from the query
        match = re.search(r'from\s+(\w+)\s+to\s+(\w+)', query)
        if match:
            source = match.group(1).capitalize()
            destination = match.group(2).capitalize()
            print(f"Parsed source: {source}, destination: {destination}")

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)

            sql_query = """
                SELECT bus_name, departure_time, arrival_time, fare, bus_type, stops 
                FROM buses 
                WHERE source=%s AND destination=%s
            """
            cursor.execute(sql_query, (source, destination))
            results = cursor.fetchall()
            print(f"Query results: {results}")

            if results:
                response_text = f"Available buses from {source} to {destination}:\n"
                for row in results:
                    response_text += (
                        f"{row['bus_name']} ({row['bus_type']}), Departure: {row['departure_time']}, "
                        f"Arrival: {row['arrival_time']}, Fare: Rs. {row['fare']}, Stops: {row['stops']}\n"
                    )
                return jsonify({"response": response_text})
            else:
                return jsonify({"response": f"No buses found from {source} to {destination}. Please check the route or try again."})
        else:
            print("Query did not match the expected format")
            return jsonify({"error": "Invalid query format. Please say something like 'Find bus from [source] to [destination]'."}), 400
    except mysql.connector.Error as db_err:
        print(f"Database error details: {db_err}")
        return jsonify({"error": f"Database error occurred: {str(db_err)}"}), 500
    except Exception as e:
        print(f"Unexpected server error: {e}")
        return jsonify({"error": f"Server error occurred: {str(e)}"}), 500
    finally:
        if cursor:
            cursor.close()
        if db and db.is_connected():
            db.close()
            print("Database connection closed for this request.")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
