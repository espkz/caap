from flask import Flask, render_template, request, redirect, url_for
from CAAP import *

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
            pdf_file.save('flask_site_test/uploads/' + pdf_file.filename)
            text = process_pdf('flask_site_test/uploads/' + pdf_file.filename)
            results = get_keywords(text)
            return redirect(url_for('show_results', results=results))

@app.route('/results')
def results():
    results = request.args.get('results')
    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=False)
