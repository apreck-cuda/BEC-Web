
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import subprocess
import os

app = Flask(__name__)
socketio = SocketIO(app)

script_map = {
    "Brute Force": "scripts/brute_force.sh",
    "Email Attack": "scripts/email_attack.sh",
    "Network Protection": "scripts/network_protection.sh",
    "Endpoint Virus": "scripts/endpoint_virus.sh"
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('run_script')
def handle_run_script(data):
    script_name = data.get('script')
    script_path = script_map.get(script_name)

    if script_path and os.path.exists(script_path):
        process = subprocess.Popen(['bash', script_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        with process.stdout:
            for line in iter(process.stdout.readline, ''):
                print(line, end='')  # Print to server terminal
                emit('terminal_output', {'output': line})
                socketio.sleep(0)  # Yield to event loop for real-time updates
        process.wait()
        print(f"\nScript '{script_name}' finished.\n")
        emit('terminal_output', {'output': f"\nScript '{script_name}' finished.\n"})
    else:
        print(f"Script '{script_name}' not found.\n")
        emit('terminal_output', {'output': f"Script '{script_name}' not found.\n"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
