import mysql.connector
from mysql.connector import Error
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # MySQL username
            password='root',  # MySQL password
            database='E_Learning'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

# Fetch all courses
def get_courses():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM COURSES")
            courses = cursor.fetchall()
            cursor.close()
            connection.close()
            return courses
        else:
            return {"error": "Database connection failed"}
    except Exception as e:
        print(f"Error fetching courses: {e}")
        return {"error": str(e)}

# Fetch all students
def get_students():
    try:
        connection = create_connection()
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM STUDENTS")
            students = cursor.fetchall()
            cursor.close()
            connection.close()
            return students
        else:
            return {"error": "Database connection failed"}
    except Exception as e:
        print(f"Error fetching students: {e}")
        return {"error": str(e)}

# Request handler for the HTTP server
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/courses':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            courses = get_courses()
            self.wfile.write(json.dumps(courses, default=str).encode())

        elif self.path == '/students':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            students = get_students()
            self.wfile.write(json.dumps(students, default=str).encode())

        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Page not found")

# Run the server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
