# Architecture

This project is intentionally small for the Challenge 01 MVP.

Flow:

```txt
CLI -> Capture -> SQLite -> Statistics
```

Responsibilities:

- `app/cli.py`: command-line argument parsing and user-facing CLI flow.
- `app/capture.py`: offline pcap reading and live packet capture with Scapy.
- `app/storage.py`: SQLite schema creation and packet insertion.
- `app/statistics.py`: SQL-based summary statistics and terminal formatting.
- `tests/`: automated tests for CLI behavior and future business logic.

The CLI decides the input source:

- when `--pcap-file` is provided, packets are read from that file;
- otherwise, when `--interface` is provided, packets are captured live;
- when neither is provided, the command returns a friendly usage error.

Captured packet metadata is normalized before storage. The application stores only timestamp, source IP, destination IP, protocol, and packet size. Raw packet payloads are not saved.

Out of scope for this challenge:

- web frontend
- web API
- dashboard
- authentication
- external services
- external database
- ORM
