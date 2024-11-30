from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return render_template('result.html', result=result)
    except subprocess.CalledProcessError as e:
        return render_template('result.html', error=e.stderr)

if __name__ == '__main__':
    app.run(debug=True)