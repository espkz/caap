from flask import Flask, render_template, request, redirect, url_for
from CAAP import *
import ast

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['pdfFile']
        if pdf_file:
            pdf_file.save('flask_site_test/static/uploads/' + pdf_file.filename)
            text = process_pdf('flask_site_test/static/uploads/' + pdf_file.filename)
            keywords = get_keywords(text)
            results = get_definitions(keywords)
            pdf_url = url_for('static', filename='uploads/' + pdf_file.filename)
            return redirect(url_for('results', results=results, pdf_url = pdf_url))

@app.route('/results')
def results():
    results = request.args.get('results')
    if type(results) is str:
        results = ast.literal_eval(results)

    pdf_url = request.args.get('pdf_url')
    return render_template('results.html', results=results, pdf_url=pdf_url)

if __name__ == '__main__':
    app.run(debug=False)
