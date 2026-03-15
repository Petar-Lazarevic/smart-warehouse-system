"""
@file app.py
@author Petar Lazarevic
@brief Web dashboard for real-time warehouse inventory monitoring.
@details Flask application that fetches RFID logs from SQLite and calculates item statistics.
"""

from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    """
    Establishes a connection to the SQLite database.
    Configures row_factory to return dictionary-like objects for easier data access.
    """
    conn = sqlite3.connect('warehouse.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """
    Main dashboard route. Handles search queries, fetches logs, 
    and generates real-time statistics.
    """
    # Retrieve search query from URL parameters (if any)
    query = request.args.get('search', '')
    conn = get_db_connection()
    
    if query:
        # Search logs by item name or RFID ID
        sql = "SELECT * FROM logs WHERE item LIKE ? OR rfid_id LIKE ? ORDER BY id DESC"
        logs = conn.execute(sql, ('%'+query+'%', '%'+query+'%')).fetchall()
    else:
        # Fetch all records ordered by the most recent entry
        logs = conn.execute('SELECT * FROM logs ORDER BY id DESC').fetchall()
    
    # Counting occurrences for each unique item in the current view
    stats = {}
    for log in logs:
        item = log['item']
        stats[item] = stats.get(item, 0) + 1
        
    conn.close()
    
    # Render UI with data, computed stats, and the persistent search term
    return render_template('index.html', logs=logs, stats=stats, query=query)

if __name__ == '__main__':
    # Start the Flask server on all available network interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
