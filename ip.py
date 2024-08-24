from flask import Flask, render_template, request
import requests
import socket

app = Flask(__name__)

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error as err:
        return None

def fetch_ip_info(ip):
    try:
        response = requests.get(f"https://ipinfo.io/{ip}/json")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.RequestException:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    ip_info = None
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Check if the query is an IP address or a hostname
            try:
                socket.inet_aton(query)  # Validate IP address
                ip = query
            except socket.error:
                ip = get_ip_from_hostname(query)
            # Fetch IP information
            if ip:
                ip_info = fetch_ip_info(ip)
    return render_template('index.html', ip_info=ip_info)

if __name__ == '__main__':
    # Run the Flask application on 0.0.0.0 and port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
