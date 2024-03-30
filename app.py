from flask import Flask, render_template

app = Flask(__name__)
app = Flask(__name__, static_folder='assets')
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def upload():
    return render_template('about.html')

@app.route('/services')
def results():
    return render_template('services.html')

if __name__ == '__main__':
    app.run(debug=True)
