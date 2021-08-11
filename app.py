from flask import Flask, redirect, render_template, request, send_from_directory
from flask_basicauth import BasicAuth
from werkzeug.utils import secure_filename
from datetime import datetime

import os

app = Flask(__name__)
UPLOAD_FOLDER = 'data'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FLASK_ADMIN_SWATCH'] = 'readable'
app.config['BASIC_AUTH_USERNAME'] = 'root'
app.config['BASIC_AUTH_PASSWORD'] = '123456'
basic_auth = BasicAuth(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        ### voice conversion ###
        return render_template("index.html", audio=True)
    return render_template('index.html', audio=False)


@app.route("/download/<path:filename>")
def downloader(filename):
    dirpath = app.root_path + "/" + UPLOAD_FOLDER
    return send_from_directory(dirpath, filename, as_attachment=True)


@app.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return "no file"
        file = request.files['file']
        if file.filename == '':
            return "no file name"
        if file:
            _ = secure_filename(file.filename)
            file.save(os.path.join(
                app.config['UPLOAD_FOLDER'], "recorder.wav"))
    return render_template('index.html')


def main():
    os.makedirs("data", exist_ok=True)
    app.run()
    # app.run(host='0.0.0.0', port=12345, debug=False)


if __name__ == '__main__':
    # supervisorctl stop all
    # supervisorctl reload
    main()
