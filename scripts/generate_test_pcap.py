"""Generate a small reproducible pcap file for offline tests."""

from __future__ import annotations

import argparse
from pathlib import Path

from scapy.all import ICMP, IP, TCP, UDP, wrpcap


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a small pcap file with TCP, UDP, and ICMP packets."
    )
    parser.add_argument(
        "--output",
        default="samples/test.pcap",
        help="Output pcap path. Default: samples/test.pcap.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    packets = [
        IP(src="192.168.0.10", dst="8.8.8.8") / TCP(sport=12345, dport=443),
        IP(src="192.168.0.20", dst="1.1.1.1") / UDP(sport=5353, dport=53),
        IP(src="192.168.0.30", dst="8.8.4.4") / ICMP(),
    ]

    wrpcap(str(output_path), packets)
    print(f"Generated pcap: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
