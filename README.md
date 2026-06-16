# meli-traffic-challenge

Python CLI project for a technical focused on Support / Infrastructure.

The application will later capture network packets, save traffic data in SQLite, and display basic statistics. This initial version only provides the project structure and a prepared CLI.

## Scope

Included:

- Python CLI using `argparse`
- Optional offline pcap input with `--pcap-file`
- Basic project layout with `app/`, `tests/`, and `docs/`
- Dockerfile
- Initial tests

Not included:

- frontend
- web API
- dashboard
- authentication
- real packet capture

## Requirements

- Python 3.12+

## Setup

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

## Usage

```bash
python -m app.main --interface eth0 --timeout 60 --count 100 --db-path traffic.db
```

Offline pcap mode for future tests:

```bash
python -m app.main --pcap-file samples/capture.pcap --db-path traffic.db
```

Available arguments:

- `--interface`: network interface name
- `--timeout`: maximum capture time in seconds
- `--count`: maximum number of packets
- `--db-path`: SQLite database path
- `--pcap-file`: optional pcap file path for offline testing

## Tests

```bash
pytest
```

## Docker

```bash
docker build -t meli-traffic-challenge .
docker run --rm meli-traffic-challenge --timeout 10 --count 5
```
