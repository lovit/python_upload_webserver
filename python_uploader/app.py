import argparse
import os
from flask import Flask, request, redirect, url_for
from waitress import serve
from werkzeug.utils import secure_filename


app = Flask(__name__)


HTML_TEMPLATE = """
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form action="" method=post enctype=multipart/form-data>
  <p><input type=file name=file>
     <input type=submit value=Upload>
</form>
<h2>File list at {}</h2>
<p>{}</p>"""

def listdir(root):
    def get_humanize_size(name):
        path = os.path.join(root, name)
        s = os.stat(path).st_size
        if s < 1024:
            return f"{s} byte"
        if s < 1048576:
            return f"{int(s / 1024)} Kb"
        if s < 1073741824:
            return f"{int(s / 1048576)} Mb"
        return f"{int(s / 1073741824)} Gb"

    ROW_FORMAT = '<tr><td>{}</td><td style="text-align:left">{}</td><td>{}</td></tr>'
    filenames = sorted([name for name in os.listdir(root) if os.path.isfile(f'{root}/{name}')])
    dirnames = sorted([name for name in os.listdir(root) if os.path.isdir(f'{root}/{name}')])

    rows = [ROW_FORMAT.format('DIR', name, ' - ') for name in dirnames]
    rows += [ROW_FORMAT.format('FILE', name, get_humanize_size(name)) for name in filenames]
    table = '<table>{}</table>'.format('\n'.join(rows))
    return table


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('index'))
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    HTML = HTML_TEMPLATE.format(UPLOAD_FOLDER, listdir(UPLOAD_FOLDER))
    return HTML


def main():
    parser = argparse.ArgumentParser(description='File uploader app ')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Default is localhost')
    parser.add_argument('--port', type=int, default=5000, help='(default %(default)s)')
    parser.add_argument('--debug', dest='debug', action='store_true', help='Debug Flask app')
    parser.add_argument('--max_size', type=int, default=1024, help='MB (default %(default)s)')
    parser.add_argument('--upload_folder', default='./', help='Default save folder (default %(default)s)')

    args = parser.parse_args()
    UPLOAD_FOLDER = os.path.abspath(args.upload_folder)
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = args.max_size * 1024 * 1024
    print(f'Upload destination : {UPLOAD_FOLDER}')
    print(f'Maximum size       : {args.max_size} MB')

    if args.debug:
        app.run(host=args.host, port=args.port, debug=True)
    else:
        serve(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
