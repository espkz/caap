from flask import Flask, render_template

app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=False)
