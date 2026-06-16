# Architecture

This project is intentionally small for the first implementation stage.

Planned responsibilities:

- `app/cli.py`: command-line argument parsing and user-facing CLI flow.
- packet capture module: future live capture and offline pcap reading.
- storage module: future SQLite persistence.
- statistics module: future traffic summaries and reporting.
- `tests/`: automated tests for CLI behavior and future business logic.

Out of scope for this challenge:

- web frontend
- web API
- dashboard
- authentication
- external services

