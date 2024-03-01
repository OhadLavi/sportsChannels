from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key

# The HTML content for the login page
LOGIN_PAGE = """
<!doctype html>
<title>Login</title>
<h2>Login</h2>
<form method="post">
    <label for="password">Password:</label>
    <input type="password" id="password" name="password">
    <input type="submit" value="Login">
</form>
"""

# The HTML template for the protected page
PROTECTED_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sports Channels</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #343a40;
            color: #fff;
        }
        .container {
            padding-top: 20px;
        }
        .video-container {
            text-align: center;
        }
        .video {
            width: 736.94px;
            height: 500px;
            margin: 0 auto;
        }
        .channel-title {
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Sports Channels</h1>
        {% for channel in channels %}
        <h2 class="channel-title">{{ channel.name }}</h2>
        <div class="video-container">
            <iframe class="video responsive" loading="lazy" marginheight="0" marginwidth="0" width="736.94" height="500" src="{{ channel.src }}" name="iframe_a" scrolling="no" allowfullscreen="yes" frameborder="0"></iframe>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

# Replace 'your_password' with your desired password
CORRECT_PASSWORD = 'your_password'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == CORRECT_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('protected'))
        else:
            return 'Incorrect password!', 403
    return LOGIN_PAGE

@app.route('/')
def protected():
    if not session.get('authenticated'):
        return redirect(url_for('login'))

    channels = [
        {'name': 'Sport 1', 'src': 'https://dlhd.sx/embed/stream-140.php'},
        {'name': 'Sport 2', 'src': 'https://dlhd.sx/embed/stream-141.php'},
        # Add more channels as needed
    ]
    
    return render_template_string(PROTECTED_PAGE, channels=channels)

if __name__ == '__main__':
    app.run(debug=True)
