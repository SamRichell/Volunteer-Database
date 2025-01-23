<?php

session_start();

$_SESSION["logged_in"] = FALSE;

// Creates PDO object telling it it's and sqlite db at such location
$DB_con = new PDO("sqlite:VolunteerDB.sqlite3");

// Query the database
$statement = $DB_con->query("SELECT ParticipationName FROM PreferredParticipation");

// Retrieve what database returns
$results = $statement->fetchAll(PDO::FETCH_ASSOC);

// define preferred participation array
$PP = array();

for ($count=0; $count<count($results); $count++) {
    array_push($PP, $results[$count]["ParticipationName"]);
};

?>

<html>
    <head>
        <title>Sign Up</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div class="banner">
            <a href="Login Page.php">Log In</a>
            <span>Lightwater Connected</span>
        </div>
        <div class="content_box">
            <h1>Sign Up</h1>
            <form action="Sign Up.php" method="POST">
                <label for="forename">Forename:
                <input type="text" id="forename" name="forename" required pattern="([a-z]|[A-Z])+"></label><br>
                <label for="surname">Surname:
                <input type="text" id="surname" name="surname" required pattern="([a-z]|[A-Z])+"></label><br>
                <label for="email">Email:
                <input type="email" id="email" name="email" required></label><br>
                <label for="password">Password:
                <input type="password" id="password" name="password" required pattern=".{8,100}" title="Must be between 8 and 100 characters"></label><br>
                <label for="phone_number">Phone Number:
                <input type="text" id="phone_number" name="phone_number" required pattern="(07)[0-9]{9}" title="Enter a valid UK mobile number"></label><br>
                <label for="address">Address:
                <input type="text" id="address" name="address" required></label><br>
                <label for="postcode">Postcode:
                <input type="text" id="postcode" name="postcode" required pattern="([A-Z]|[A-Z][A-Z])([1-9][A-Z]?|[1-9][1-9]) [0-9][A-Z][A-Z]" title="Enter a valid postcode (including a space)"></label><br>
                <h2>Preferred Participation</h2>
                <label for="subtext">Please Select atleast one</label>
                <?php
                for ($count=0; $count<count($PP); $count++) {
                    $to_output = $PP[$count];
                    echo "<label for='$to_output'><input type='checkbox' id='$to_output' name='$to_output'> $to_output</label>";
                };
                ?>
                <input type="submit" value="Submit">
            </form>
        </div>
    </body>
</html>

<?php

function phpAlert($msg) {
    echo '<script type="text/javascript">alert("' . $msg . '")</script>';
};

if (isset($_SESSION["entered_PP"])) {
    if ($_SESSION["entered_PP"] == FALSE) {
        phpAlert("Please select atleast one preferred participation option");
    };
};

$_SESSION["entered_PP"] = TRUE;

?>