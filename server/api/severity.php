<?php
require '../db.php';
header('Content-Type: application/json');

$stmt = $db->query("SELECT severity, COUNT(*) as count FROM logs GROUP BY severity");
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($results);
