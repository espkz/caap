from flask import Flask, render_template, request, redirect, url_for, session
from CAAP import *
import ast

app = Flask(__name__, template_folder='templates')
app.secret_key = 'caap_cs_329'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/set_tier', methods=['POST'])
def set_tier():
    tier = request.form.get('tier', type=int)
    session['tier'] = tier
    return 'SUCCESS'

@app.route('/update_definitions', methods=['POST'])
def update_definitions():
    keywords = request.form['keywords']
    text = request.form['text']
    if type(keywords) is str:
        keywords = keywords.replace('{', '[')
        keywords = keywords.replace('}', ']')
        keywords = ast.literal_eval(keywords)
    tier = int(request.form['tier'])
    if keywords is not None:
        updated_definitions = get_definitions(keywords, tier, text)
    else:
        updated_definition = ""
    return render_template('definitions.html', results = updated_definitions, definitions=updated_definitions)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        pdf_file = request.files['pdfFile']
        if pdf_file:
            pdf_file.save('flask_site_test/static/uploads/' + pdf_file.filename)
            text = process_pdf('flask_site_test/static/uploads/' + pdf_file.filename)
            keywords = get_keywords(text)
            pdf_url = url_for('static', filename='uploads/' + pdf_file.filename)
            return redirect(url_for('results', keywords = keywords, pdf_url = pdf_url,text = text))

@app.route('/results')
def results():
    tier = session.get('tier', 1)
    keywords = request.args.get('keywords')
    text = request.args.get('text')
    if type(keywords) is str:
        keywords = keywords.replace('{', '[')
        keywords = keywords.replace('}', ']')
        keywords = ast.literal_eval(keywords)
    results = None
    if keywords:
        print("Tier: " + str(tier))
        results = get_definitions(keywords, tier, text)
        if type(results) is str:
            results = ast.literal_eval(results)

    pdf_url = request.args.get('pdf_url')
    return render_template('results.html', keywords = keywords, results=results, pdf_url=pdf_url, tier = tier, text = text)

if __name__ == '__main__':
    app.run(debug=True)
