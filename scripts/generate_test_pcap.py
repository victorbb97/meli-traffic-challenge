"""Generate a reproducible pcap file for offline demonstrations."""

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

    top_sources = [
        ("10.0.0.1", 12),
        ("10.0.0.2", 10),
        ("10.0.0.3", 8),
        ("10.0.0.4", 6),
        ("10.0.0.5", 5),
    ]
    extra_sources = [(f"10.0.1.{index}", 1) for index in range(1, 16)]
    source_pool = [
        source
        for source, occurrences in top_sources + extra_sources
        for _ in range(occurrences)
    ]

    top_destinations = [
        ("203.0.113.10", 13),
        ("203.0.113.20", 11),
        ("203.0.113.30", 9),
        ("203.0.113.40", 7),
        ("203.0.113.50", 6),
    ]
    extra_destinations = [(f"198.51.100.{index}", 1) for index in range(1, 11)]
    destination_pool = [
        destination
        for destination, occurrences in top_destinations + extra_destinations
        for _ in range(occurrences)
    ]

    packets = []
    for index, (source, destination) in enumerate(zip(source_pool, destination_pool)):
        if index % 3 == 0:
            packet = IP(src=source, dst=destination) / TCP(
                sport=10000 + index,
                dport=443,
            )
        elif index % 3 == 1:
            packet = IP(src=source, dst=destination) / UDP(
                sport=20000 + index,
                dport=53,
            )
        else:
            packet = IP(src=source, dst=destination) / ICMP()

        packets.append(packet)

    wrpcap(str(output_path), packets)
    print(f"Generated pcap: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
