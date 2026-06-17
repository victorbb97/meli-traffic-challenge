"""Packet capture and pcap reading helpers."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def extract_packet_data(packet: Any) -> dict[str, Any]:
    """Extract the required fields from a Scapy packet."""
    from scapy.layers.inet import ICMP, IP, TCP, UDP
    from scapy.layers.inet6 import IPv6

    source_ip = None
    destination_ip = None
    protocol = "NON_IP"

    if packet.haslayer(IP):
        ip_layer = packet[IP]
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst
    elif packet.haslayer(IPv6):
        ip_layer = packet[IPv6]
        source_ip = ip_layer.src
        destination_ip = ip_layer.dst

    if source_ip is not None or destination_ip is not None:
        if packet.haslayer(TCP):
            protocol = "TCP"
        elif packet.haslayer(UDP):
            protocol = "UDP"
        elif packet.haslayer(ICMP):
            protocol = "ICMP"
        else:
            protocol = "IP"

    return {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "source_ip": source_ip,
        "destination_ip": destination_ip,
        "protocol": protocol,
        "packet_size": len(packet),
    }


def read_packets_from_pcap(pcap_file: str) -> list[dict[str, Any]]:
    """Read packets from a pcap file and return normalized packet records."""
    from scapy.all import rdpcap

    packets = rdpcap(pcap_file)
    return [extract_packet_data(packet) for packet in packets]


def capture_packets(interface: str, timeout: int, count: int) -> list[dict[str, Any]]:
    """Capture packets from a live network interface."""
    from scapy.all import sniff

    packets = sniff(iface=interface, timeout=timeout, count=count)
    return [extract_packet_data(packet) for packet in packets]

