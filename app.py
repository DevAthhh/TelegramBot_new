from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        if request.form['start'] == '90':
            print(request.form['start'])
            return render_template('index.html', title='Данные отправлены')
    else:
        return render_template('index.html', title='No')

if __name__ == '__main__':
    app.run(debug=True)