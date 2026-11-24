<?php
require 'db.php';
header('Content-Type: application/json');

$key = $_SERVER['HTTP_X_API_KEY'] ?? '';

if ($key !== 'key123') {
    http_response_code(401);
    echo json_encode(['error' => 'invalid api key']);
    exit;
} 

$raw = file_get_contents('php://input');

$data = json_decode($raw, TRUE);  

if (!is_array($data) || !isset($data['agent_id']) || !isset($data['message'])) {
    http_response_code(400);
    echo json_encode(['error' => 'invalid payload']);
    exit;
}   

$stmt = $db->prepare("
    INSERT INTO logs (agent_id, username, timestamp, source, event_type, source_ip, message, severity)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
");

$stmt->execute([
    $data['agent_id'],
    $data['username']   ?? 'unknown', 
    $data['timestamp']  ?? date('c'),
    $data['source']     ?? 'unknown',
    $data['event_type'] ?? 'unknown',
    $data['source_ip']  ?? null,
    $data['message'],
    $data['severity']   ?? 'info',
]);

echo json_encode([
    'status' => 'ok',
    'id'     => $db->lastInsertId()
]);
