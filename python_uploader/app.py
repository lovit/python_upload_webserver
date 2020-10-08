import argparse
import os
from flask import Flask, request, redirect, url_for
from waitress import serve
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    return """
    <!doctype html>
    <title>Upload a file</title>
    <h1>Upload a file</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))


def main():
    parser = argparse.ArgumentParser(description='MT-Eval flask app ')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Default is localhost')
    parser.add_argument('--port', type=int, default=5000, help='Default is :5000')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Debug Flask app')
    parser.add_argument('--upload_folder', default='/tmp/', help='Default save folder')

    args = parser.parse_args()
    UPLOAD_FOLDER = os.path.abspath(args.upload_folder)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    print(f'Upload destination : {UPLOAD_FOLDER}')

    if args.debug:
        app.run(host=args.host, port=args.port, debug=True)
    else:
        serve(app, port=args.port)

if __name__ == "__main__":
    main()
