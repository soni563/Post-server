from flask import Flask, request, render_template_string, jsonify
import requests
from time import sleep
import threading
import os

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

stop_flag = threading.Event()
status_messages = []

@app.route('/', methods=['GET', 'POST'])
def send_comment():
    global status_messages
    status_messages = []

    if request.method == 'POST':
        datr = request.form.get('datr')
        post_id = request.form.get('postId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        cookies = {
            'datr': datr
        }

        def send_messages():
            global status_messages
            while not stop_flag.is_set():
                try:
                    for message1 in messages:
                        if stop_flag.is_set():
                            break
                        api_url = f'https://www.facebook.com/api/graphql/'
                        message = str(mn) + ' ' + message1
                        parameters = {
                            'av': '',  # You might need to retrieve this value dynamically.
                            '__user': '',  # You might need to retrieve this value dynamically.
                            '__a': 1,
                            'fb_dtsg': '',  # You might need to retrieve this value dynamically.
                            'jazoest': '',  # You might need to retrieve this value dynamically.
                            'doc_id': 'ID_OF_THE_GRAPHQL_DOC_FOR_COMMENTING',  # You need to find this value.
                            'variables': '{"input":{"client_mutation_id":"X","actor_id":"","message":{"text":"'+message+'"},"feedback_id":"'+post_id+'"}}'
                        }
                        response = requests.post(api_url, data=parameters, headers=headers, cookies=cookies)
                        if response.status_code == 200:
                            status_messages.append(f"Comment sent: {message}")
                        else:
                            status_messages.append(f"Failed to send comment: {message}")
                        sleep(time_interval)
                except Exception as e:
                    status_messages.append(f"Error: {str(e)}")
                    sleep(30)

        thread = threading.Thread(target=send_messages)
        thread.start()

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ArYan.x3</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {
                background-color: pink;
            }
            .container {
                max-width: 500px;
                background-color: #fff;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                margin: 0 auto;
                margin-top: 20px;
            }
            .header {
                text-align: center;
                padding-bottom: 20px;
            }
            .btn-submit {
                width: 100%;
                margin-top: 10px;
            }
            .footer {
                text-align: center;
                margin-top: 20px;
                color: #888;
            }
            .status {
                margin-top: 20px;
                background-color: #f8f9fa;
                padding: 10px;
                border-radius: 5px;
                max-height: 200px;
                overflow-y: auto;
            }
        </style>
        <script>
            async function fetchStatus() {
                const response = await fetch('/status');
                const status = await response.json();
                const statusDiv = document.getElementById('status');
                statusDiv.innerHTML = '';
                status.forEach(msg => {
                    const p = document.createElement('p');
                    p.textContent = msg;
                    statusDiv.appendChild(p);
                });
            }
            setInterval(fetchStatus, 1000);
        </script>
    </head>
    <body>
        <header class="header mt-4">
            <h1 class="mb-3">ArYan.x3</h1>
            <p>PosT Server</p>
            <h1 class="mt-3">OWNER :: ArYan</h1>
        </header>

        <div class="container">
            <form action="/" method="post" enctype="multipart/form-data">
                <div class="mb-3">
                    <label for="datr">Enter Your datr cookie:</label>
                    <input type="text" class="form-control" id="datr" name="datr" required>
                </div>
                <div class="mb-3">
                    <label for="postId">Enter Post ID:</label>
                    <input type="text" class="form-control" id="postId" name="postId" required>
                </div>
                <div class="mb-3">
                    <label for="kidx">Enter Hater Name:</label>
                    <input type="text" class="form-control" id="kidx" name="kidx" required>
                </div>
                <div class="mb-3">
                    <label for="txtFile">Select Your Notepad File:</label>
                    <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
                </div>
                <div class="mb-3">
                    <label for="time">Speed in Seconds:</label>
                    <input type="number" class="form-control" id="time" name="time" required>
                </div>
                <button type="submit" class="btn btn-primary btn-submit">Submit Your Details</button>
            </form>
        </div>
        <div class="container mt-3">
            <form action="/stop" method="post">
                <button type="submit" class="btn btn-danger btn-submit">Stop</button>
            </form>
        </div>
        <div class="container mt-3 status" id="status">
            <!-- Status messages will be displayed here -->
        </div>
        <footer class="footer">
            <p>&copy; 2023 ArYan.x3 All Rights Reserved.</p>
            <p>Convo/Inbox Loader Tool</p>
            <p>Made with Anonymous Rullex  by <a href="https://github.com/SK-BAAP-786">SK-BAAP-786</a></p>
        </footer>
    </body>
    </html>
    ''')

@app.route('/status', methods=['GET'])
def status():
    global status_messages
    return jsonify(status_messages)

@app.route('/stop', methods=['POST'])
def stop():
    stop_flag.set()
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if shutdown:
        shutdown()
    return 'Server shutting down...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)
