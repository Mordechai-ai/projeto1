import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'hewqia23e'

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')  # Diretório para salvar os arquivos enviados
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/your-url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('This ShortName has already been taken. Choose another one!')
            return redirect(url_for('home'))

        if 'url' in request.form.keys():
            urls[request.form['code']] = {'Url': [request.form['url']]}
        else:
            f = request.files['file']
            if f.filename == '':
                flash('No file selected')
                return redirect(url_for('home'))

            full_name = request.form['code'] + secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], full_name)
            f.save(file_path)
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)

        return render_template('your_url.html', code=request.form['code'])
    else:
        return redirect(url_for('home'))


@app.route('/<string:code>')
def redirect_to_url(code):
    if os.path.exists('urls.json'):
        with open('urls.json') as urls_file:
            urls = json.load(urls_file)
            if code in urls.keys():
                if 'Url' in urls[code].keys():
                    return redirect(urls[code]['Url'][0])
                elif 'file' in urls[code].keys():
                    return send_from_directory(app.config['UPLOAD_FOLDER'], urls[code]['file'])
    return redirect(url_for('home'))






if __name__ == "__main__":
    app.run(debug=True)