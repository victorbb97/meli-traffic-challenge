"""Command-line interface for meli-traffic-challenge."""

from __future__ import annotations

import argparse
import sys

from app.capture import capture_packets, read_packets_from_pcap
from app.statistics import calculate_statistics, format_statistics
from app.storage import initialize_database, insert_packets


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="meli-traffic-challenge",
        description=(
            "Capture or read network packets, save them in SQLite, and show "
            "basic traffic statistics."
        ),
    )

    parser.add_argument(
        "--interface",
        help="Network interface to capture from, for example eth0 or Wi-Fi.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Maximum capture time in seconds. Default: 60.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=100,
        help="Maximum number of packets to process. Default: 100.",
    )
    parser.add_argument(
        "--db-path",
        default="traffic.db",
        help="SQLite database path. Default: traffic.db.",
    )
    parser.add_argument(
        "--pcap-file",
        help="Optional pcap file path for offline testing.",
    )

    return parser


def run(args: argparse.Namespace) -> int:
    """Run the CLI command."""
    if not args.pcap_file and not args.interface:
        print(
            "Error: provide --pcap-file for offline analysis or --interface "
            "for live capture.",
            file=sys.stderr,
        )
        return 2

    try:
        if args.pcap_file:
            packets = read_packets_from_pcap(args.pcap_file)
        else:
            packets = capture_packets(args.interface, args.timeout, args.count)

        initialize_database(args.db_path)
        insert_packets(args.db_path, packets)
        summary = calculate_statistics(args.db_path)
        print(format_statistics(summary))
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and execute the command."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)
