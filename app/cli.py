"""Command-line interface for meli-traffic-challenge."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="meli-traffic-challenge",
        description=(
            "Prepare network traffic capture settings. Real packet capture "
            "will be implemented in a future version."
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
    print("meli-traffic-challenge")
    print("Network packet capture is not implemented yet.")
    print(f"Interface: {args.interface or 'not provided'}")
    print(f"Timeout: {args.timeout} seconds")
    print(f"Packet count: {args.count}")
    print(f"Database path: {args.db_path}")

    if args.pcap_file:
        print(f"Offline pcap file: {args.pcap_file}")
    else:
        print("Offline pcap file: not provided")

    return 0


def main(argv: list[str] | None = None) -> int:
    """Parse CLI arguments and execute the command."""
    parser = build_parser()
    args = parser.parse_args(argv)
    return run(args)

