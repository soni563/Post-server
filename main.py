from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ayushii iinsiide ❤️</title>
        <style>
            body {
                margin: 0;
                font-family: Arial, sans-serif;
                background-image: url('https://i.ibb.co/CtywLqd/ca1a82d4e26b4183884555c42bf52e4b.jpg');
                background-size: cover;
                background-repeat: no-repeat;
                background-position: center;
                color: white;
            }
            .container {
                text-align: center;
                padding: 50px;
            }
            .title {
                font-size: 2em;
                margin-bottom: 20px;
                color: blue;
            }
            .subtitle {
                font-size: 1.5em;
                margin-bottom: 40px;
                color: red;
            }
            .form-container {
                background: rgba(0, 0, 0, 0.5);
                padding: 20px;
                border-radius: 10px;
                display: inline-block;
            }
            input[type="text"], input[type="file"], input[type="number"] {
                display: block;
                margin: 10px auto;
                padding: 10px;
                width: 80%;
                max-width: 300px;
            }
            input[type="submit"] {
                background-color: green;
                color: white;
                border: none;
                padding: 15px 30px;
                cursor: pointer;
                font-size: 1em;
                border-radius: 5px;
            }
            .warrior-rulex {
                background-color: red;
                color: white;
                padding: 10px;
                border-radius: 5px;
                margin-top: 20px;
                display: inline-block;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="subtitle">(😈 SILENT QUEEN SONII 😈)</div>
            <div class="form-container">
                <form action="/submit" method="post" enctype="multipart/form-data">
                    <input type="text" name="post_id" placeholder="Post ID" required><br>
                    <input type="text" name="hater_name" placeholder="Enter Hater Name" required><br>
                    <input type="file" name="np_file" required><br>
                    <input type="file" name="tokens_file" required><br>
                    <input type="number" name="speed" min="20" placeholder="Speed in Seconds (minimum 20 seconds)" required><br>
                    <input type="submit" value="Submit Your Details">
                </form>
                <div class="All Rulex cHod">😈All in One 😈<br>Unstoppble Ayushii 😋</div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/submit', methods=['POST'])
def submit():
    post_id = request.form['post_id']
    hater_name = request.form['hater_name']
    np_file = request.files['np_file']
    tokens_file = request.files['tokens_file']
    speed = request.form['speed']

    # Process the uploaded files and form data here
    # For example, save the files and handle the data as needed
    np_file.save(f'uploads/{np_file.filename}')
    tokens_file.save(f'uploads/{tokens_file.filename}')

    return f"Details Submitted: Post ID = {post_id}, Hater Name = {hater_name}, Speed = {speed} seconds"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
