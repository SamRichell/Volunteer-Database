<?php

session_start();

// Ensure user has already logged in
if ($_SESSION["logged_in"] == TRUE) {
    $DB_con = new PDO("sqlite:VolunteerDB.sqlite3");

    $ID = $_SESSION["VolunteerID"];

    $find_user_statement = $DB_con->query("SELECT Volunteers.Forename, Volunteers.Surname, Volunteers.Email, Volunteers.Password, Volunteers.MobileNumber, Volunteers.Address, Volunteers.Postcode, PreferredParticipation.ParticipationName FROM Volunteers, PreferredParticipation, ParticipationAssignment WHERE Volunteers.VolunteerID=ParticipationAssignment.VolunteerID AND ParticipationAssignment.ParticipationID=PreferredParticipation.ParticipationID AND Volunteers.VolunteerID=$ID");

    $volunteer_results = $find_user_statement->fetchAll(PDO::FETCH_ASSOC);

    $volunteer_details = $volunteer_results[0];

    $forename = $volunteer_details["Forename"];
    $surname = $volunteer_details["Surname"];
    $email = $volunteer_details["Email"];
    $password = $volunteer_details["Password"];
    $phone_number = $volunteer_details["MobileNumber"];
    $address = $volunteer_details["Address"];
    $postcode = $volunteer_details["Postcode"];

    $num_of_participation = count($volunteer_results);
    $selected_PP = array($volunteer_details["ParticipationName"]);

    for ($count=1; $count<$num_of_participation; $count++) {
        array_push($selected_PP, $volunteer_results[$count]["ParticipationName"]);
    };

    $find_PP_statement = $DB_con->query("SELECT ParticipationName FROM PreferredParticipation");

    $PP_results = $find_PP_statement->fetchAll(PDO::FETCH_ASSOC);

    $PP = array();

    for ($count=0; $count<count($PP_results); $count++) {
        array_push($PP, $PP_results[$count]["ParticipationName"]);
    };

} else {
    header("Location: Login Page.php");
};

?>
<html>
    <head>
        <title>Settings</title>
        <link rel="stylesheet" type="text/css" href="style.css">
    </head>
    <body>
        <div class="banner">
            <a href="Sign Out.php">Sign Out</a>
            <span>Lightwater Connected</span>
        </div>
        <div class="content_box">
            <h1>Welcome <?php echo "$forename"?></h1>
            <form action="Update Details.php" method="POST">
                <label for="forename">Forename: <?php echo "$forename" ?></label>
                <input type="text" id="forename" name="forename" pattern="([a-z]|[A-Z])+"><br><br>
                <label for="surname">Surname: <?php echo "$surname" ?></label>
                <input type="text" id="surname" name="surname" pattern="([a-z]|[A-Z])+"><br><br>
                <label for="email">Email: <?php echo "$email" ?></label>
                <input type="email" id="email" name="email"><br><br>
                <label for="password">Password: <?php echo "$password" ?></label>
                <input type="password" id="password" name="password" pattern=".{8,100}" title="Must be between 8 and 100 characters"><br><br>
                <label for="phone_number">Phone Number: 0<?php echo "$phone_number" ?></label>
                <input type="text" id="phone_number" name="phone_number" pattern="07[0-9].{8}" title="Enter a valid UK mobile number"><br><br>
                <label for="address">Address: <?php echo "$address" ?></label>
                <input type="text" id="address" name="address"><br><br>
                <label for="postcode">Postcode: <?php echo "$postcode" ?></label>
                <input type="text" id="postcode" name="postcode" pattern="([A-Z]|[A-Z][A-Z])([1-9][A-Z]?|[1-9][1-9]) [0-9][A-Z][A-Z]" title="Enter a valid postcode (including a space)"><br><br>
                <?php
                for ($count=0; $count<count($PP); $count++) {
                    $to_output = $PP[$count];
                    if (in_array($to_output, $selected_PP)) {
                        echo "<label for='$to_output'><input type='checkbox' id='$to_output' name='$to_output' checked> $to_output</label>";
                    } else {
                        echo "<label for='$to_output'><input type='checkbox' id='$to_output' name='$to_output'> $to_output</label>";
                    };
                };
                ?>
                <input type="submit" value="Submit">
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