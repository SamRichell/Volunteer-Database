<?php

session_start();

// Ensure user has entered preferred participation
if (count($_POST) < 8) {
    $_SESSION["entered_PP"] = FALSE;
    header("Location: Settings Page.php");
    exit;
};

// Creates PDO object telling it it's and sqlite db at such location
$DB_con = new PDO("sqlite:VolunteerDB.sqlite3");

// Retrieving values entered by user on 
$ID = $_SESSION["VolunteerID"];
$forename = $_POST["forename"];
$surname = $_POST["surname"];
$email = $_POST["email"];
$password = $_POST["password"];
$phone_number = $_POST["phone_number"];
$address = $_POST["address"];
$postcode = $_POST["postcode"];

// Finding users current details
$find_user_statement = $DB_con->query("SELECT Forename, Surname, Email, Password, MobileNumber, Address, Postcode FROM Volunteers WHERE VolunteerID=$ID");

$user_results = $find_user_statement->fetchAll(PDO::FETCH_ASSOC);

// Ensuring no values are left empty
if ($forename == "") {
    $forename = $user_results[0]["Forename"];
};
if ($surname == "") {
    $surname = $user_results[0]["Surname"];
};
if ($email == "") {
    $email = $user_results[0]["Email"];
};
if ($password == "") {
    $password = $user_results[0]["Password"];
};
if ($phone_number == "") {
    $phone_number = $user_results[0]["MobileNumber"];
};
if ($address == "") {
    $address = $user_results[0]["Address"];
};
if ($postcode == "") {
    $postcode = $user_results[0]["Postcode"];
};

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

    // Delete current Details
    $delete_PP_statement = $DB_con->prepare("DELETE FROM ParticipationAssignment WHERE VolunteerID=?");
    $delete_PP_statement->execute([$ID]);
    $delete_volunteer_statement = $DB_con->prepare("DELETE FROM Volunteers WHERE VolunteerID=?");
    $delete_volunteer_statement->execute([$ID]);

    // Insert statement prepared
    $prepared_statement = $DB_con->prepare("INSERT INTO Volunteers (VolunteerID, Forename, Surname, Email, Password, MobileNumber, Address, Postcode) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");

    // Values added into insert statement
    // Insert statement executed returns true if completed and false if error
    $completed = $prepared_statement->execute([$ID, $forename, $surname, $email, $password, $phone_number, $address, $postcode]);

    for ($count=0; $count<count($selected_PP); $count++) {
        // Preparing the insert statement for the selected Preferred Participation
        $PP_prepared_statement = $DB_con->prepare("INSERT INTO ParticipationAssignment (VolunteerID, ParticipationID) VALUES (?, ?)");
        //Executing the statement
        $PP_prepared_statement->execute([$ID, $selected_PP[$count]]);
    };
};

header("Location: Settings Page.php");

?>