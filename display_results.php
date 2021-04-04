<?php
$servername = "sql6.freemysqlhosting.net";
$dbUsername = "sql6403319";
$dbPassword = "jkb1mBQnaG";
$dbName = "sql6403319";

$conn = mysqli_connect($servername, $dbUsername, $dbPassword, $dbName);
if (!$conn) {
    die("connection failed" . mysqli_connect_error());
}

if (!isset($_GET['examcode'])) {
    die("Add 'examcode=' get parameter in url");
}

$exam_code = mysqli_real_escape_string($conn, $_GET['examcode']);
$sql = '';
$isAsc = isset($_GET['order']) ? (bool) $_GET['order'] : 1;
if (isset($_GET['sort'])) {
    $sql = "select * from " . $exam_code . " order by -`" . mysqli_real_escape_string($conn, $_GET['sort']) . "` " . ($isAsc ? 'ASC' : 'DESC') . " ;";
} else {
    $sql = "select * from " . $exam_code . " order by rollno";
}

$exam_result = mysqli_query($conn, $sql);
if (mysqli_num_rows($exam_result) <= 0) {
    die("0 results");
}

$subjects_result = mysqli_query($conn, "select * from `subject_names` where `exam_code`='" . $exam_code . "';");
mysqli_close($conn);
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <title>3-1 Results</title>
    <style>
        table {
            border-collapse: collapse;
            width: 100%;
            color: #588c7e;
            font-family: monospace;
            font-size: 14px;
            text-align: center;
        }
        .more-space{
            background-color: #588c7e;
            color: white;
            padding-right: 20px;
            padding-left: 20px;
        }
        a{
            color: white;
        }
        th {
            background-color: #588c7e;
            color: white;
            padding-right: 5px;
        }
        tr:nth-child(even) {background-color: #f2f2f2}
    </style>
</head>
<body>
<table>
    <tr>
        <th class="more-space"><a href='display_results.php?examcode=<?php echo $exam_code; ?>&sort=rollno&order=<?php echo $isAsc ?>'>Rollno</a></th>
        <th class="more-space"><a href='display_results.php?examcode=<?php echo $exam_code; ?>&sort=name&order=<?php echo $isAsc ?>'>Name</a></th>
        <?php
        while ($row = mysqli_fetch_assoc($exam_result)) {
            echo "<th><a href='display_results.php?examcode=" . $exam_code . "&sort=" . $row['subject_code'] . "&order=" . $isAsc . "'>" . mysqli_fetch_row($subjects_result)[3] . "</a></th>";
        }
        ?>
        <th><a href='display_results.php?examcode=<?php echo $exam_code; ?>&sort=grade&order=<?php echo $isAsc ?>'>grade</a></th>
    </tr>
    <?php
    while ($row = mysqli_fetch_assoc($exam_result)) {
        echo "<tr>";
        foreach ($row as $col) {
            echo "<td>" . $col . "</td>";
        }
        echo "</tr>";
    }
    ?>
</table>
</body>
</html>
