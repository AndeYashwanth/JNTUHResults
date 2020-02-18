<?php
require "../includes/dbh.inc.php"; //connectiont to database. It contains $conn
$sql='';
$isAsc = isset($_GET['order'])? (bool) $_GET['order']: 1;
if (isset($_GET['sort'])) {
    $sql = "select * from results_32 order by -`".$_GET['sort']."` ".($isAsc?'ASC':'DESC')." ;";
} else{
    $sql = "select * from results_32 order by rollno";
}
$result = mysqli_query($conn, $sql);
mysqli_close($conn);
?>
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
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
        <th class="more-space"><a href='31_results.php?sort=rollno&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>Rollno</a></th>
        <th class="more-space"><a href='31_results.php?sort=name&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>Name</a></th>
        <th><a href='31_results.php?sort=13508&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>COMPUTER NETWORKS LAB</a></th>
        <th><a href='31_results.php?sort=13510&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>DESIGN AND ANALYSIS OF ALGORITHMS LAB</a></th>
        <th><a href='31_results.php?sort=13534&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>SOFTWARE ENGINEERING LAB</a></th>
        <th><a href='31_results.php?sort=13537&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>PROFESSIONAL ETHICS</a></th>
        <th><a href='31_results.php?sort=135AE&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>DATA COMMUNICATION AND COMPUTER NETWORKS</a></th>
        <th><a href='31_results.php?sort=135AF&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>DESIGN AND ANALYSIS OF ALGORITHMS</a></th>
        <th><a href='31_results.php?sort=135AR&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>FUNDAMENTALS OF MANAGEMENT</a></th>
        <th><a href='31_results.php?sort=135BM&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>SOFTWARE ENGINEERING</a></th>
        <th><a href='31_results.php?sort=135CX&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>PRINCIPLES OF ELECTRONIC COMMUNICATIONS</a></th>
        <th><a href='31_results.php?sort=grade&order=<?php echo isset($_GET['order'])?!$_GET['order']:1; ?>'>grade</a></th>
    </tr>
    <?php
    if (mysqli_num_rows($result) > 0) {
        while($rows = mysqli_fetch_assoc($result)) {
            echo "<tr>";
            foreach ($rows as $row){
                echo "<td>".$row."</td>";
            }
            echo "</tr>";
        }
    } else {
        echo "0 results";
    }
    ?>
    <!--    <br><br>-->
    <!--    <p>Add someone</p>-->
</table>
</body>
</html>
