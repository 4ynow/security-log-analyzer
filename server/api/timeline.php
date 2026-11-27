<?php
require '../db.php';
header('Content-Type: application/json');

$stmt = $db->query("SELECT strftime('%H:00', timestamp) as time, COUNT(*) as count FROM logs GROUP BY time ORDER BY time ASC");
$results = $stmt->fetchAll(PDO::FETCH_ASSOC);

echo json_encode($results);
