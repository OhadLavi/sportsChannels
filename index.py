from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = 'replace_with_a_secure_secret_key'

# Define a list of channels with their names and URLs
channels = [
    {'name': 'Sport 1', 'url': 'https://dlhd.sx/embed/stream-140.php'},
    {'name': 'Sport 2', 'url': 'https://dlhd.sx/embed/stream-141.php'},
    {'name': 'Sport 3', 'url': 'https://dlhd.sx/embed/stream-142.php'},
    {'name': 'Sport 4', 'url': 'https://dlhd.sx/embed/stream-143.php'},
    {'name': 'Sport 5', 'url': 'https://dlhd.sx/embed/stream-144.php'},
    {'name': 'Sport 5 Plus', 'url': 'https://dlhd.sx/embed/stream-148.php'},
    {'name': 'Sport 5 Gold', 'url': 'https://dlhd.sx/embed/stream-145.php'},
    # Add more channels as needed
]

# HTML template for the login page
login_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <form method="POST">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password">
        <input type="submit" value="Login">
    </form>
</body>
</html>
'''

# HTML template for the protected page
protected_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <title>Protected Content</title>
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
            <iframe class="video responsive" loading="lazy" marginheight="0" marginwidth="0" width="736.94" height="500" src="{{ channel.url }}" name="iframe_a" scrolling="no" allowfullscreen="yes" frameborder="0"></iframe>
        </div>
        {% endfor %}
    </div>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        # Replace 'your_password' with your actual password
        if password == 'hapoel':
            session['authenticated'] = True
            return redirect(url_for('protected'))
        else:
            return 'Incorrect password', 401
    return login_page_html

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
def protected():
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    # Pass the channels list to the template
    return render_template_string(protected_page_html, channels=channels)

if __name__ == '__main__':
    app.run(debug=True)
