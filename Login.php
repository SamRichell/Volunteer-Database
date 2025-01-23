<?php

// Starting a session allows variables to be used in other programs
session_start();

$DB_con = new PDO("sqlite:VolunteerDB.sqlite3");

// Collect inputed email and password from login page
$email = $_POST["email"];
$password = $_POST["password"];

// SQL statment to find user
$select_statement = $DB_con->query("SELECT VolunteerID, Email FROM Volunteers WHERE Email='$email' AND Password='$password'");

// Results returned as array
$results = $select_statement->fetchAll(PDO::FETCH_ASSOC);

if ($results[0]["Email"] == $email) {

    $_SESSION["logged_in"] = TRUE;
    $_SESSION["VolunteerID"] = $results[0]["VolunteerID"];

    header("Location: Settings Page.php");
} else {
    header("Location: Login Page.php");
};

?>