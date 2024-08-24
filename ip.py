from flask import Flask, render_template_string, request
import requests
import socket

app = Flask(__name__)

def get_ip_from_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.error:
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

# Define the HTML template directly in the app.py file
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IP Geolocator</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            max-width: 600px;
            margin: auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .result {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>IP Geolocator</h1>
        <form method="POST">
            <label for="query">Enter an IP address or hostname:</label>
            <input type="text" id="query" name="query" required>
            <button type="submit">Get Info</button>
        </form>

        {% if ip_info %}
        <div class="result">
            <h2>Information for {{ ip_info.ip }}</h2>
            <p><strong>Hostname:</strong> {{ ip_info.hostname }}</p>
            <p><strong>City:</strong> {{ ip_info.city }}</p>
            <p><strong>Region:</strong> {{ ip_info.region }}</p>
            <p><strong>Country:</strong> {{ ip_info.country }}</p>
            <p><strong>Location:</strong> {{ ip_info.loc }}</p>
            <p><strong>Organization:</strong> {{ ip_info.org }}</p>
            <p><strong>Postal:</strong> {{ ip_info.postal }}</p>
            <p><strong>Timezone:</strong> {{ ip_info.timezone }}</p>
            <p><a href="{{ ip_info.readme }}">More Info</a></p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

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
    return render_template_string(HTML_TEMPLATE, ip_info=ip_info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
