<?php

$db = new PDO('sqlite:' . __DIR__ . '/db/siem.db');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$db->exec("
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        agent_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        source TEXT NOT NULL,
        event_type TEXT NOT NULL,
        source_ip TEXT,
        message TEXT NOT NULL,
        severity TEXT DEFAULT 'info'
    )
");
