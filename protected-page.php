<?php
session_start();

// Redirect to login if not authenticated
if (!isset($_SESSION['authenticated']) || !$_SESSION['authenticated']) {
    header('Location: login.php');
    exit;
}

// Assuming authentication is successful, generate the content.
$channels = [
    ['number' => 140, 'name' => 'Sport 1'],
    ['number' => 141, 'name' => 'Sport 2'],
    ['number' => 142, 'name' => 'Sport 3'],
    ['number' => 143, 'name' => 'Sport 4'],
    ['number' => 144, 'name' => 'Sport 5'],
    // Assuming you skip 146 and 147 intentionally
    ['number' => 148, 'name' => 'Sport 5 Plus'],
    ['number' => 145, 'name' => 'Sport 5 Gold'],
];

?>
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
            text-align: center; /* Center iframe container */
        }
        .video {
            width: 736.94px;
            height: 500px; /* Increased height */
            margin: 0 auto; /* Center iframe horizontally */
        }
        .channel-title {
            margin-top: 20px;
            margin-bottom: 10px;
            text-align: center; /* Center titles */
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="text-center mb-4">Sports Channels</h1>
        <div id="channels">
            <?php foreach ($channels as $channel): ?>
                <h2 class="channel-title"><?= htmlspecialchars($channel['name']); ?></h2>
                <div class="video-container">
                    <iframe class="video responsive" loading="lazy" marginheight="0" marginwidth="0" width="736.94" height="500" src="https://dlhd.sx/embed/stream-<?= htmlspecialchars($channel['number']); ?>.php" name="iframe_a" scrolling="no" allowfullscreen="yes" frameborder="0"></iframe>
                </div>
            <?php endforeach; ?>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
</body>
</html>
