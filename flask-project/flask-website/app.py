from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services/<service_name>')
def service(service_name):
    return render_template('service.html', service_name=service_name)

@app.route('/products/<product_category>')
def product(product_category):
    return render_template('product.html', product_category=product_category)
    
@app.route('/signin')
def signin():
    return render_template('signin1.html')


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)