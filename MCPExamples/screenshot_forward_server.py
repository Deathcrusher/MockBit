import io
import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    forward_url = request.form.get('forward_url') or os.environ.get('DEFAULT_FORWARD_URL')
    if not file:
        return jsonify({'error': 'No file'}), 400
    data = file.read()
    if forward_url:
        # Forward screenshot to the requesting LLM via MCP
        resp = requests.post(forward_url, files={'file': ('screenshot.png', data, 'image/png')})
        return jsonify({'forward_status': resp.status_code})
    return jsonify({'received': len(data)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
