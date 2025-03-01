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
    {'name': 'Sport 5 Plus', 'url': 'https://dlhd.sx/embed/stream-145.php'},
    {'name': 'Sport 5 Gold', 'url': 'https://dlhd.sx/embed/stream-148.php'},
    # Add more channels as needed
]

# HTML template for the login page
login_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #343a40;
            color: #fff;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .login-container {
            background-color: rgba(0, 0, 0, 0.5);
            border-radius: 10px;
            padding: 30px;
            width: 90%;
            max-width: 400px;
        }
        .form-control {
            margin-bottom: 15px;
        }
        .btn-primary {
            width: 100%;
            background-color: #007bff;
            border: none;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2 class="text-center mb-4">Login</h2>
        <form method="POST">
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password" class="form-control" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
    </div>
</body>
</html>
'''

# HTML template for the protected page
protected_page_html = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sports Channels</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
    <style>
        body {
            background-color: #343a40;
            color: #fff;
            padding-bottom: 20px;
        }
        .container {
            padding-top: 20px;
        }
        .video-container {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
            margin-bottom: 30px;
        }
        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        .channel-title {
            margin-top: 20px;
            margin-bottom: 15px;
            text-align: center;
            font-size: 1.5rem;
        }
        .channel-nav {
            background-color: #212529;
            overflow-x: auto;
            white-space: nowrap;
            padding: 10px 0;
            margin-bottom: 20px;
            -webkit-overflow-scrolling: touch;
        }
        .channel-nav a {
            display: inline-block;
            color: #fff;
            text-align: center;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 20px;
            margin: 0 5px;
            transition: background-color 0.3s;
        }
        .channel-nav a:hover, .channel-nav a.active {
            background-color: #007bff;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            background-color: #212529;
        }
        .logout-btn {
            color: #fff;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 5px;
            background-color: #dc3545;
        }
        .ad-blocker-notice {
            background-color: #28a745;
            color: white;
            text-align: center;
            padding: 5px;
            font-size: 0.9rem;
            margin-bottom: 10px;
        }
        .iframe-overlay {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: transparent;
            z-index: 10;
            pointer-events: none;
        }
        @media (max-width: 576px) {
            .channel-title {
                font-size: 1.2rem;
            }
            .container {
                padding-left: 5px;
                padding-right: 5px;
            }
        }
    </style>
    <!-- Meta tags to discourage ads -->
    <meta name="robots" content="nofollow">
    <meta http-equiv="Content-Security-Policy" content="frame-src 'self' dlhd.sx; default-src 'self' 'unsafe-inline' stackpath.bootstrapcdn.com cdnjs.cloudflare.com code.jquery.com cdn.jsdelivr.net dlhd.sx;">
</head>
<body>
    <div class="header">
        <h1 class="m-0">Sports Channels</h1>
        <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
    
    <div class="ad-blocker-notice">
        <i class="fas fa-shield-alt"></i> Ad blocking enabled
    </div>
    
    <div class="channel-nav" id="channelNav">
        {% for channel in channels %}
        <a href="#channel-{{ loop.index }}" class="{% if loop.first %}active{% endif %}">{{ channel.name }}</a>
        {% endfor %}
    </div>
    
    <div class="container">
        {% for channel in channels %}
        <div id="channel-{{ loop.index }}" class="channel-section">
            <h2 class="channel-title">{{ channel.name }}</h2>
            <div class="video-container">
                <iframe loading="lazy" src="{{ channel.url }}" name="iframe_{{ loop.index }}" allowfullscreen="yes" sandbox="allow-scripts allow-same-origin allow-forms"></iframe>
                <div class="iframe-overlay"></div>
            </div>
        </div>
        {% endfor %}
    </div>
    
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Highlight active channel in navigation
        const navLinks = document.querySelectorAll('.channel-nav a');
        
        // Add click event to navigation links
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            });
        });
        
        // Scroll to active channel on page load
        document.addEventListener('DOMContentLoaded', function() {
            const firstChannel = document.getElementById('channel-1');
            if (firstChannel) {
                firstChannel.scrollIntoView();
            }
        });
        
        // Block popup ads
        (function() {
            // Override window.open to prevent popups
            const originalWindowOpen = window.open;
            window.open = function() {
                console.log('Popup blocked');
                return null;
            };
            
            // Block new tabs/windows
            document.addEventListener('click', function(e) {
                if (e.target.tagName === 'A' && e.target.target === '_blank') {
                    e.preventDefault();
                    console.log('New tab/window blocked');
                }
            }, true);
            
            // Block iframe redirects
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                try {
                    iframe.onload = function() {
                        try {
                            // Try to access iframe content (may fail due to same-origin policy)
                            const iframeWindow = iframe.contentWindow;
                            const originalIframeOpen = iframeWindow.open;
                            iframeWindow.open = function() {
                                console.log('Iframe popup blocked');
                                return null;
                            };
                        } catch (e) {
                            // Cannot access iframe content due to same-origin policy
                            console.log('Cannot access iframe content');
                        }
                    };
                } catch (e) {
                    console.log('Error setting up iframe protection', e);
                }
            });
        })();
    </script>
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
