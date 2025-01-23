<?php

session_start();

if ($_SESSION["logged_in"] == TRUE) {
    header("Location: Settings Page.php");
};

?>


<html>
    <head>
        <title>Login Page</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div class="banner">
            <a href="Sign Up Page.php">Sign Up</a>
            <span>Lightwater Connected</span>
        </div>
        <div class="content_box">
            <h1>Login</h1>
            <form action="Login.php" method="POST">
                <label for="email">Email: <input type="text" id="email" name="email"></label><br><br>
                <label for="password">Password: <input type="password" id="password" name="password"></label><br><br>
                <input type="submit" value="Submit">
            </form> 
        </div>
    </body>
</html>