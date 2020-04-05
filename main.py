# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import flask
import io

from flask import current_app, flash, Flask, Markup, redirect, render_template, send_file
from flask import request, url_for
from PyPDF2 import PdfFileMerger, PageRange

app = Flask(__name__)
app.config.update(
    ALLOWED_EXTENSIONS=set(['pdf'])
)

app.debug = False
app.testing = False


@app.route('/')
def home():
    return render_template('list.html')


@app.route('/merge', methods=['POST'])
def uploadpdf():
    # If an image was uploaded, update the data to point to the new image.
    uploaded_files = flask.request.files.getlist("file[]")
    pdffiles = [f for f in uploaded_files if f.filename.endswith((".pdf"))]
    print 'murugaaaaaaaa'
    merger = PdfFileMerger()
    output = io.BytesIO()

    count = 0;
    for pdf in pdffiles:
        print(pdf)
        count = count + 1
        # merger.append(pdffile, pages=PageRange('1:-1'))
        merger.append(pdf)

    print merger.__sizeof__()

    if count > 0:
        merger.write("result.pdf")
        merger.close()
        return send_file("result.pdf", as_attachment=True)

    return "Invalid files"


@app.route('/errors')
def errors():
    raise Exception('This is an intentional exception.')


# This is only used when running locally. When running live, gunicorn runs
# the application.
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
