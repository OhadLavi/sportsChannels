from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
# Set a secure secret key
app.secret_key = 'replace_with_a_secure_secret_key'

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
</head>
<body>
    <h1>Welcome to the Protected Page</h1>
    <p>This content is only visible to authenticated users.</p>
</body>
</html>
'''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        # Replace 'your_password' with your actual password
        if password == 'your_password':
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
    return protected_page_html

if __name__ == '__main__':
    app.run(debug=True)
