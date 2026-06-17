"""Traffic statistics based on captured packet records."""

from __future__ import annotations

import sqlite3
from typing import Any


def calculate_statistics(db_path: str) -> dict[str, Any]:
    """Calculate summary statistics from the SQLite packets table."""
    with sqlite3.connect(db_path) as connection:
        total_packets = connection.execute(
            "SELECT COUNT(*) FROM packets"
        ).fetchone()[0]
        packets_by_protocol = connection.execute(
            """
            SELECT protocol, COUNT(*) AS packet_count
            FROM packets
            GROUP BY protocol
            ORDER BY packet_count DESC, protocol ASC
            """
        ).fetchall()
        top_source_ips = connection.execute(
            """
            SELECT source_ip, COUNT(*) AS packet_count
            FROM packets
            WHERE source_ip IS NOT NULL
            GROUP BY source_ip
            ORDER BY packet_count DESC, source_ip ASC
            LIMIT 5
            """
        ).fetchall()
        top_destination_ips = connection.execute(
            """
            SELECT destination_ip, COUNT(*) AS packet_count
            FROM packets
            WHERE destination_ip IS NOT NULL
            GROUP BY destination_ip
            ORDER BY packet_count DESC, destination_ip ASC
            LIMIT 5
            """
        ).fetchall()

    return {
        "total_packets": total_packets,
        "packets_by_protocol": packets_by_protocol,
        "top_source_ips": top_source_ips,
        "top_destination_ips": top_destination_ips,
    }


def format_statistics(summary: dict[str, Any]) -> str:
    """Format traffic statistics for terminal output."""
    lines = [
        "=== Traffic Analysis Summary ===",
        "",
        f"Total packets captured: {summary['total_packets']}",
        "",
        "Packets by protocol:",
    ]

    for protocol, packet_count in summary["packets_by_protocol"]:
        lines.append(f"{protocol}: {packet_count}")

    lines.extend(["", "Top 5 source IPs:"])
    for position, (source_ip, packet_count) in enumerate(
        summary["top_source_ips"], start=1
    ):
        lines.append(f"{position}. {source_ip} - {packet_count} packets")

    lines.extend(["", "Top 5 destination IPs:"])
    for position, (destination_ip, packet_count) in enumerate(
        summary["top_destination_ips"], start=1
    ):
        lines.append(f"{position}. {destination_ip} - {packet_count} packets")

    return "\n".join(lines)
