"""SQLite storage helpers for captured packets."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS packets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    captured_at TEXT NOT NULL,
    source_ip TEXT,
    destination_ip TEXT,
    protocol TEXT NOT NULL,
    packet_size INTEGER NOT NULL
);
"""


def initialize_database(db_path: str) -> None:
    """Create the SQLite database schema if needed."""
    path = Path(db_path)
    if path.parent != Path("."):
        path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as connection:
        connection.execute(SCHEMA)
        connection.commit()


def insert_packets(db_path: str, packets: list[dict[str, Any]]) -> None:
    """Insert normalized packet records into SQLite."""
    with sqlite3.connect(db_path) as connection:
        connection.executemany(
            """
            INSERT INTO packets (
                captured_at,
                source_ip,
                destination_ip,
                protocol,
                packet_size
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    packet["captured_at"],
                    packet["source_ip"],
                    packet["destination_ip"],
                    packet["protocol"],
                    packet["packet_size"],
                )
                for packet in packets
            ],
        )
        connection.commit()

