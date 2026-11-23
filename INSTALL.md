# Installation

## Requirements

- PHP 8.0 or newer
- PHP SQLite driver (`pdo_sqlite`)

## Install

### Debian / Ubuntu / Kali

```bash
sudo apt update
sudo apt install php php-cli php-sqlite3
```

### Verify

```bash
php -v
php -m | grep -i sqlite
```

Both `sqlite3` and `pdo_sqlite` must appear in the second command's output.

## Run

From the project root:

```bash
php -S 0.0.0.0:8080
```

Then open:

```text
http://127.0.0.1:8080/server/db.php
```

A blank page means the server and database are working.

## Common errors

- `could not find driver`: the PHP SQLite driver is missing. Install `php-sqlite3`.
- `php: command not found`: PHP is not installed.
