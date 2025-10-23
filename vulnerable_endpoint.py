# FILE: vulnerable_endpoint.py

import os
from flask import Flask, request

# Initialize a simple Flask application
app = Flask(__name__)

@app.route("/api/ping", methods=["GET"])
def ping_server():
    """
    VULNERABLE ENDPOINT: Uses external input directly in an OS shell command.
    """
    # 1. Get user input from the URL query parameters
    hostname = request.args.get('host')
    
    if not hostname:
        return "Error: Missing 'host' parameter", 400

    # 2. [VULNERABLE SINK] Pass unsanitized input to os.system()
    # A hacker can submit: 127.0.0.1; whoami
    # The application will execute 'ping -c 1 127.0.0.1' followed by 'whoami'
    command = f"ping -c 1 {hostname}"
    
    # Snyk Code should flag the os.system() call as a critical vulnerability source.
    os.system(command) # <-- The "Sink" where the vulnerability is exploited
    
    return f"Attempted to ping host: {hostname}"

if __name__ == "__main__":
    app.run(debug=True)