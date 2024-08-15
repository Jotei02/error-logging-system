from flask import Flask, request, jsonify
import psycopg2
import logging
from logging.handlers import RotatingFileHandler
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Database connection
def get_db_connection():
    return psycopg2.connect(
        dbname='your_db_name',
        user='your_db_user',
        password='your_db_password',
        host='your_db_host'
    )

# Email notification setup
def send_error_email(error_message):
    msg = MIMEText(error_message)
    msg['Subject'] = 'Critical Error in Flask Application'
    msg['From'] = 'your_email@example.com'
    msg['To'] = 'admin@example.com'

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('your_email@example.com', 'your_email_password')
        server.sendmail('your_email@example.com', 'admin@example.com', msg.as_string())

# Error logging route
@app.errorhandler(Exception)
def handle_exception(e):
    error_message = str(e)
    error_trace = str(e.__traceback__)
    url = request.url
    method = request.method
    user_agent = request.headers.get('User-Agent')
    status_code = 500

    # Log error to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO error_logs (error_message, error_trace, url, method, user_agent, status_code)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (error_message, error_trace, url, method, user_agent, status_code))
    conn.commit()
    cursor.close()
    conn.close()

    # Send email for critical errors
    if status_code == 500:
        send_error_email(error_message)

    # Return JSON response
    return jsonify(error="An internal error occurred"), status_code

# Log rotation setup
handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)

@app.route('/')
def index():
    return 'Welcome to the Flask App!'

@app.route('/error')
def error():
    # Intentional error for demonstration
    return 1 / 0

if __name__ == '__main__':
    app.run(debug=True)
