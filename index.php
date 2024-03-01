<?php
session_start();

// Redirect to the protected page if already logged in
if (isset($_SESSION['authenticated']) && $_SESSION['authenticated']) {
    header('Location: protected-page.php');
    exit;
}

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $passwordEntered = $_POST['password'];
    $correctPassword = 'yourSecurePassword'; // Replace with your actual password

    if ($passwordEntered === $correctPassword) {
        $_SESSION['authenticated'] = true;
        header('Location: protected-page.php');
        exit;
    } else {
        $error = 'Incorrect password!';
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body>
    <?php if ($error): ?>
        <p><?php echo $error; ?></p>
    <?php endif; ?>
    <form method="post">
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <button type="submit">Login</button>
    </form>
</body>
</html>
