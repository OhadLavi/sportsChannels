from flask import Flask, request, redirect, url_for, session, render_template_string
import os

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
            font-family: Arial, sans-serif;
            padding-top: 110px; /* Space for fixed header and nav */
        }
        .container {
            padding-top: 20px;
            max-width: 100%;
            padding-left: 10px;
            padding-right: 10px;
        }
        .video-container {
            position: relative;
            padding-bottom: 56.25%; /* 16:9 aspect ratio */
            height: 0;
            overflow: hidden;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            max-width: 800px; /* Limit max width */
            max-height: 450px; /* Limit max height */
            margin-left: auto;
            margin-right: auto;
        }
        @media (min-width: 1200px) {
            .video-container {
                padding-bottom: 0;
                height: 450px;
            }
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
            color: #fff;
            text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
        }
        .nav-wrapper {
            position: fixed;
            top: 50px; /* Below the header */
            left: 0;
            right: 0;
            z-index: 99;
        }
        .channel-nav {
            background-color: #212529;
            overflow-x: auto;
            white-space: nowrap;
            padding: 10px 0;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: thin;
            scrollbar-color: #007bff #212529;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        }
        .channel-nav::-webkit-scrollbar {
            height: 6px;
        }
        .channel-nav::-webkit-scrollbar-thumb {
            background-color: #007bff;
            border-radius: 3px;
        }
        .channel-nav::-webkit-scrollbar-track {
            background-color: #212529;
        }
        .channel-nav a {
            display: inline-block;
            color: #fff;
            text-align: center;
            padding: 8px 16px;
            text-decoration: none;
            border-radius: 20px;
            margin: 0 5px;
            transition: all 0.3s;
            font-size: 0.9rem;
        }
        .channel-nav a:hover, .channel-nav a.active {
            background-color: #007bff;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,123,255,0.5);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 15px;
            background-color: #212529;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 100;
        }
        .header h1 {
            font-size: 1.5rem;
            margin: 0;
        }
        .logout-btn {
            color: #fff;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 5px;
            background-color: #dc3545;
            transition: all 0.3s;
            font-size: 0.9rem;
        }
        .logout-btn:hover {
            background-color: #c82333;
            color: #fff;
            text-decoration: none;
            transform: translateY(-2px);
        }
        .popup-blocker-notice {
            background-color: #28a745;
            color: white;
            text-align: center;
            padding: 5px;
            font-size: 0.9rem;
            position: fixed;
            top: 50px;
            left: 0;
            right: 0;
            z-index: 98;
        }
        @media (max-width: 576px) {
            .channel-title {
                font-size: 1.2rem;
            }
            .header h1 {
                font-size: 1.2rem;
            }
            .logout-btn {
                font-size: 0.8rem;
                padding: 4px 8px;
            }
            .channel-nav a {
                padding: 6px 12px;
                font-size: 0.8rem;
            }
            body {
                padding-top: 100px;
            }
        }
        .channel-section {
            scroll-margin-top: 120px; /* Ensures proper scrolling with sticky header */
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Sports Channels</h1>
        <a href="{{ url_for('logout') }}" class="logout-btn"><i class="fas fa-sign-out-alt"></i> Logout</a>
    </div>
    
    <div class="popup-blocker-notice">
        <i class="fas fa-shield-alt"></i> Popup blocking enabled
    </div>
    
    <div class="nav-wrapper">
        <div class="channel-nav" id="channelNav">
            {% for channel in channels %}
            <a href="#channel-{{ loop.index }}" class="{% if loop.first %}active{% endif %}">{{ channel.name }}</a>
            {% endfor %}
        </div>
    </div>
    
    <div class="container">
        {% for channel in channels %}
        <div id="channel-{{ loop.index }}" class="channel-section">
            <h2 class="channel-title">{{ channel.name }}</h2>
            <div class="video-container">
                <iframe loading="lazy" src="{{ channel.url }}" name="iframe_{{ loop.index }}" allowfullscreen="yes" allow="autoplay; fullscreen"></iframe>
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
            link.addEventListener('click', function(e) {
                e.preventDefault();
                navLinks.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
                
                // Smooth scroll to the target
                const targetId = this.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth' });
                }
            });
        });
        
        // Scroll to active channel on page load
        document.addEventListener('DOMContentLoaded', function() {
            const firstChannel = document.getElementById('channel-1');
            if (firstChannel) {
                setTimeout(() => {
                    firstChannel.scrollIntoView({ behavior: 'smooth' });
                }, 300);
            }
        });
        
        // Block popups
        (function() {
            // Override window.open to prevent popups
            const originalOpen = window.open;
            window.open = function() {
                console.log('Popup blocked');
                return null;
            };
            
            // Block target="_blank" links
            document.addEventListener('click', function(e) {
                if (e.target.tagName === 'A' && e.target.getAttribute('target') === '_blank') {
                    e.preventDefault();
                    console.log('New tab blocked');
                }
            }, true);
            
            // Try to block popups from iframes
            const iframes = document.querySelectorAll('iframe');
            iframes.forEach(iframe => {
                iframe.onload = function() {
                    try {
                        iframe.contentWindow.open = function() {
                            return null;
                        };
                    } catch (e) {
                        // Cannot access iframe content due to same-origin policy
                    }
                };
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

# For Render deployment
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
