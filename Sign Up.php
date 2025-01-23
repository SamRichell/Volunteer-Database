<?php

session_start();

// Ensure user has entered preferred participation
if (count($_POST) < 8) {
    $_SESSION["entered_PP"] = FALSE;
    header("Location: Sign Up Page.php");
    exit;
};

// Creates PDO object telling it it's and sqlite db at such location
$DB_con = new PDO("sqlite:VolunteerDB.sqlite3");

// Retrieving values entered by user on 
$forename = $_POST["forename"];
$surname = $_POST["surname"];
$email = $_POST["email"];
$password = $_POST["password"];
$phone_number = $_POST["phone_number"];
$address = $_POST["address"];
$postcode = $_POST["postcode"];

// Append all sellected preferred participation to an array
$selected_PP = array();

// Select all preferred participation from DB
$PP_results = $DB_con->query("SELECT ParticipationName, ParticipationID FROM PreferredParticipation")->fetchAll(PDO::FETCH_ASSOC);

// Append all selected preferred participation into list
for ($count=0; $count<count($PP_results); $count++) {
    $PP = $PP_results[$count]["ParticipationName"];
    $PP_ID = $PP_results[$count]["ParticipationID"];
    $PP_underscore = str_replace(" ", "_", $PP);
    if (array_key_exists($PP_underscore, $_POST)) {
        array_push($selected_PP, $PP_ID);
    };
};

// Check if email or phone number already in use
$check_statement = $DB_con->query("SELECT * FROM Volunteers WHERE Email='$email' OR MobileNumber='$phone_number'");

$check_results = $check_statement->fetchAll(PDO::FETCH_ASSOC);

// Ensures a result wasn't returned
if (count($check_results) == 0) {

    // SQL statement to find max ID
    $find_max_statement = $DB_con->query("SELECT MAX(VolunteerID) FROM Volunteers");

    // Store results as a 2D array
    $results = $find_max_statement->fetchAll(PDO::FETCH_ASSOC);

    // Finds needed value in 2D array
    $max_ID = $results[0]["MAX(VolunteerID)"];

    $new_ID = $max_ID + 1;

    // Insert statement prepared
    $prepared_statement = $DB_con->prepare("INSERT INTO Volunteers (VolunteerID, Forename, Surname, Email, Password, MobileNumber, Address, Postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");

    // Values added into insert statement
    // Insert statement executed returns true if completed and false if error
    $completed = $prepared_statement->execute([$new_ID, $forename, $surname, $email, $password, $phone_number, $address, $postcode]);

    for ($count=0; $count<count($selected_PP); $count++) {
        // Preparing the insert statement for the selected Preferred Participation
        $PP_prepared_statement = $DB_con->prepare("INSERT INTO ParticipationAssignment (VolunteerID, ParticipationID) VALUES (?, ?)");
        //Executing the statement
        $PP_prepared_statement->execute([$new_ID, $selected_PP[$count]]);
    };

    // Sends user to login page if completed and returns user to sign up page if not
    if($completed){
        header("Location: Login Page.php");
    } else{
        header("Location: Sign Up Page.php");
    };
    exit;
} else {
    header("Location: Sign Up Page.php");
    exit;
};
?>