<html>
<head>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
        }

        #result {
            font-size: 24px;
            color: #007BFF;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <?php
    if (isset($_POST['n1']) && isset($_POST['n2'])) {
        $total = $_POST['n1'] + $_POST['n2'];
        echo '<div id="result">Total: ' . $total . '</div>';
    } else {
        echo '<div id="result">Empty</div>';
    }

    if (isset($_GET['n1']) && isset($_GET['n2'])) {
        $total = $_GET['n1'] + $_GET['n2'];
        echo '<div id="result">Total: ' . $total . '</div>';
    }
    ?>
</body>
</html>
