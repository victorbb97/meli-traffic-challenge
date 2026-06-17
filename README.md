# meli-traffic-challenge

Python CLI project for a technical challenge focused on Support N2 / Infrastructure.

The application reads packets from a pcap file or captures packets from a network interface, stores normalized packet metadata in SQLite, and prints basic traffic statistics in the terminal.

## Scope

Included:

- Python CLI using `argparse`
- Offline pcap analysis with `--pcap-file`
- Live packet capture with `--interface`
- SQLite storage using the standard library `sqlite3`
- Basic terminal statistics
- Dockerfile
- Objective automated tests

Not included:

- frontend
- web API
- dashboard
- authentication
- queues
- external services
- external database
- ORM
- async processing

## Requirements

- Python 3.12+
- Scapy
- pytest for tests

Install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## CLI Usage

Help:

```bash
python -m app.main --help
```

Offline pcap analysis:

```bash
python -m app.main --pcap-file samples/capture.pcap --db-path traffic.db
```

Live capture:

```bash
python -m app.main --interface eth0 --timeout 60 --count 100 --db-path traffic.db
```

Available arguments:

- `--interface`: network interface name for live capture.
- `--timeout`: maximum live capture time in seconds.
- `--count`: maximum number of packets for live capture.
- `--db-path`: SQLite database path.
- `--pcap-file`: optional pcap file path for offline analysis.

If neither `--pcap-file` nor `--interface` is provided, the CLI returns a friendly usage error.

## Output

The terminal summary follows this shape:

```txt
=== Traffic Analysis Summary ===

Total packets captured: X

Packets by protocol:
TCP: X
UDP: X
ICMP: X
NON_IP: X

Top 5 source IPs:
1. 192.168.0.10 - X packets

Top 5 destination IPs:
1. 8.8.8.8 - X packets
```

## SQLite Schema

The application creates one table named `packets`:

```sql
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at TEXT NOT NULL,
    source_ip TEXT,
    destination_ip TEXT,
    protocol TEXT NOT NULL,
    packet_size INTEGER NOT NULL
);
```

Stored fields:

- `captured_at`: UTC timestamp generated during processing.
- `source_ip`: IPv4 or IPv6 source address, or `NULL` for non-IP packets.
- `destination_ip`: IPv4 or IPv6 destination address, or `NULL` for non-IP packets.
- `protocol`: `TCP`, `UDP`, `ICMP`, `IP`, or `NON_IP`.
- `packet_size`: packet size calculated with `len(packet)`.

The raw packet payload is not stored.

## Docker

Build:

```bash
docker build -t meli-traffic-challenge .
```

Run with a pcap file mounted from the current directory:

```bash
docker run --rm -v "$PWD:/data" meli-traffic-challenge --pcap-file /data/samples/capture.pcap --db-path /data/traffic.db
```

Run live capture in Docker on Linux:

```bash
docker run --rm --net=host --cap-add=NET_RAW --cap-add=NET_ADMIN meli-traffic-challenge --interface eth0 --timeout 60 --count 100 --db-path /tmp/traffic.db
```

Live capture can require administrator/root privileges, Npcap on Windows, or Linux capabilities such as `NET_RAW` and `NET_ADMIN`. Offline pcap mode is recommended for predictable tests and interview demonstrations.

## Tests

```bash
python -m compileall app tests
python -m pytest
```

The tests cover:

- CLI parser behavior
- SQLite schema creation
- basic packet insertion
- traffic statistics calculation

## Technical Decisions

- Scapy is used because it supports both offline pcap reading and live packet capture.
- SQLite is used through Python's standard `sqlite3` module to avoid external database setup.
- No ORM is used because the schema is small and the challenge benefits from explicit SQL.
- The architecture remains intentionally small: `CLI -> Capture -> SQLite -> Statistics`.
