## বিভিন্ন CSS ফ্রেমওয়ার্ক ব্যবহার করে Flask ফ্রন্টএন্ড স্টাইল করা

<p>আমি একটি ওয়েবসাইট তৈরি করতে চাই ফ্লাস্ক ব্যবহার করে।
কিন্তু আমি চাই, ফ্লাস্ক ব্যবহার করে আমি যে ওয়েবসাইট তৈরি করবো সেই ওয়েবসাইটের Frontend Style করার জন্য আমি Bootstrap5, Bulma css, Semantic UI, Materialize, UIKit এবং আরো অন্যান্য css framework ব্যবহার করতে চাই।
আপনি আমাকে এই সবগুলো css framework দিয়ে একটি ওয়েবপেজ ডিজাইন করে দেখান যেখানে সব css framework এর ব্যবহার এবং কিভাবে সংযোগ করতে হয় ?</p>


ফ্লাস্ক ব্যবহার করে ওয়েবসাইট তৈরি করা এবং বিভিন্ন CSS ফ্রেমওয়ার্ক ব্যবহার করে ফ্রন্টএন্ড স্টাইল করা একটি চমৎকার আইডিয়া! আমি আপনাকে একটি উদাহরণ দেখাতে পারি যেখানে আমরা Bootstrap 5, Bulma, Semantic UI, Materialize, এবং UIKit ব্যবহার করবো। 

প্রথমে, ফ্লাস্ক অ্যাপ্লিকেশন সেটআপ করার জন্য নিচের ধাপগুলো অনুসরণ করুন:

1. **ফ্লাস্ক ইনস্টল করুন**:
    ```bash
    pip install Flask
    ```

2. **প্রাথমিক ফ্লাস্ক অ্যাপ্লিকেশন তৈরি করুন**:
    ```python
    from flask import Flask, render_template

    app = Flask(__name__)

    @app.route('/')
    def home():
        return render_template('index.html')

    if __name__ == '__main__':
        app.run(debug=True)
    ```

3. **টেমপ্লেট ফোল্ডারে `index.html` ফাইল তৈরি করুন** এবং নিচের কোডটি যোগ করুন যেখানে বিভিন্ন CSS ফ্রেমওয়ার্ক ব্যবহার করা হয়েছে:

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Multi CSS Frameworks</title>
        
        <!-- Bootstrap 5 -->
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
        
        <!-- Bulma -->
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
        
        <!-- Semantic UI -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
        
        <!-- Materialize -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
        
        <!-- UIkit -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/css/uikit.min.css">
    </head>
    <body>
        <div class="container">
            <h1 class="title is-1">Hello, Flask with Multiple CSS Frameworks!</h1>
            
            <!-- Bootstrap Button -->
            <button class="btn btn-primary">Bootstrap Button</button>
            
            <!-- Bulma Button -->
            <button class="button is-primary">Bulma Button</button>
            
            <!-- Semantic UI Button -->
            <button class="ui primary button">Semantic UI Button</button>
            
            <!-- Materialize Button -->
            <button class="btn waves-effect waves-light">Materialize Button</button>
            
            <!-- UIkit Button -->
            <button class="uk-button uk-button-primary">UIkit Button</button>
        </div>
        
        <!-- Scripts for frameworks -->
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/js/uikit.min.js"></script>
    </body>
    </html>
    ```

এই উদাহরণে, আমরা বিভিন্ন CSS ফ্রেমওয়ার্কের বাটন ব্যবহার করেছি। আপনি চাইলে আরো বিভিন্ন উপাদান যোগ করতে পারেন।

---

অবশ্যই! আমি আপনাকে আরো কিছু উদাহরণ দেখাতে পারি যেখানে আমরা বিভিন্ন CSS ফ্রেমওয়ার্ক ব্যবহার করবো। নিচে কিছু অতিরিক্ত উদাহরণ দেওয়া হলো:

### উদাহরণ ১: ফর্ম ডিজাইন
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form with Multiple CSS Frameworks</title>
    
    <!-- Bootstrap 5 -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bulma -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    
    <!-- Semantic UI -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
    
    <!-- Materialize -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    
    <!-- UIkit -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/css/uikit.min.css">
</head>
<body>
    <div class="container">
        <h1 class="title is-1">Form Example</h1>
        
        <!-- Bootstrap Form -->
        <form class="mb-3">
            <div class="mb-3">
                <label for="bootstrapInput" class="form-label">Bootstrap Input</label>
                <input type="text" class="form-control" id="bootstrapInput">
            </div>
        </form>
        
        <!-- Bulma Form -->
        <form class="mb-3">
            <div class="field">
                <label class="label">Bulma Input</label>
                <div class="control">
                    <input class="input" type="text">
                </div>
            </div>
        </form>
        
        <!-- Semantic UI Form -->
        <form class="ui form mb-3">
            <div class="field">
                <label>Semantic UI Input</label>
                <input type="text">
            </div>
        </form>
        
        <!-- Materialize Form -->
        <form class="mb-3">
            <div class="input-field">
                <input id="materializeInput" type="text" class="validate">
                <label for="materializeInput">Materialize Input</label>
            </div>
        </form>
        
        <!-- UIkit Form -->
        <form class="uk-form-stacked">
            <div class="uk-margin">
                <label class="uk-form-label" for="form-stacked-text">UIkit Input</label>
                <div class="uk-form-controls">
                    <input class="uk-input" id="form-stacked-text" type="text">
                </div>
            </div>
        </form>
    </div>
    
    <!-- Scripts for frameworks -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/js/uikit.min.js"></script>
</body>
</html>
```

### উদাহরণ ২: নেভিগেশন বার ডিজাইন
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navbar with Multiple CSS Frameworks</title>
    
    <!-- Bootstrap 5 -->
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    
    <!-- Bulma -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.3/css/bulma.min.css">
    
    <!-- Semantic UI -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css">
    
    <!-- Materialize -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css">
    
    <!-- UIkit -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/css/uikit.min.css">
</head>
<body>
    <div class="container">
        <h1 class="title is-1">Navbar Example</h1>
        
        <!-- Bootstrap Navbar -->
        <nav class="navbar navbar-expand-lg navbar-light bg-light mb-3">
            <a class="navbar-brand" href="#">Bootstrap</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="#">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Features</a>
                    </li>
                </ul>
            </div>
        </nav>
        
        <!-- Bulma Navbar -->
        <nav class="navbar is-light mb-3">
            <div class="navbar-brand">
                <a class="navbar-item" href="#">Bulma</a>
            </div>
            <div class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href="#">Home</a>
                    <a class="navbar-item" href="#">Features</a>
                </div>
            </div>
        </nav>
        
        <!-- Semantic UI Navbar -->
        <div class="ui menu mb-3">
            <a class="header item" href="#">Semantic UI</a>
            <a class="item" href="#">Home</a>
            <a class="item" href="#">Features</a>
        </div>
        
        <!-- Materialize Navbar -->
        <nav class="nav-extended mb-3">
            <div class="nav-wrapper">
                <a href="#" class="brand-logo">Materialize</a>
                <ul id="nav-mobile" class="right hide-on-med-and-down">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                </ul>
            </div>
        </nav>
        
        <!-- UIkit Navbar -->
        <nav class="uk-navbar-container" uk-navbar>
            <div class="uk-navbar-left">
                <a class="uk-navbar-item uk-logo" href="#">UIkit</a>
                <ul class="uk-navbar-nav">
                    <li><a href="#">Home</a></li>
                    <li><a href="#">Features</a></li>
                </ul>
            </div>
        </nav>
    </div>
    
    <!-- Scripts for frameworks -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/5.1.3/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/js/materialize.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uikit/3.6.16/js/uikit.min.js"></script>
</body>
</html>
```

এই উদাহরণগুলোতে আমরা বিভিন্ন CSS ফ্রেমওয়ার্ক ব্যবহার করে ফর্ম এবং নেভিগেশন বার ডিজাইন করেছি। আপনি চাইলে আরো বিভিন্ন উপাদান যোগ করতে পারেন এবং আপনার প্রয়োজন অনুযায়ী কাস্টমাইজ করতে পারেন। কোনো প্রশ্ন থাকলে জানাতে পারেন! 😊

---




