<?php

require 'db.php';
header('Content-Type: application/json');

$rows = $db->query("SELECT * FROM logs ORDER BY id DESC LIMIT 100")->fetchAll(PDO::FETCH_ASSOC);
echo json_encode($rows);

