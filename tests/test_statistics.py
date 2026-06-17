from app.statistics import calculate_statistics, format_statistics
from app.storage import initialize_database, insert_packets


def test_calculate_statistics_returns_protocol_and_top_ip_counts(tmp_path):
    db_path = tmp_path / "traffic.db"
    initialize_database(str(db_path))
    insert_packets(
        str(db_path),
        [
            {
                "captured_at": "2026-06-16T18:00:00+00:00",
                "source_ip": "192.168.0.10",
                "destination_ip": "8.8.8.8",
                "protocol": "TCP",
                "packet_size": 100,
            },
            {
                "captured_at": "2026-06-16T18:00:01+00:00",
                "source_ip": "192.168.0.10",
                "destination_ip": "1.1.1.1",
                "protocol": "TCP",
                "packet_size": 120,
            },
            {
                "captured_at": "2026-06-16T18:00:02+00:00",
                "source_ip": "10.0.0.5",
                "destination_ip": "8.8.8.8",
                "protocol": "UDP",
                "packet_size": 90,
            },
            {
                "captured_at": "2026-06-16T18:00:03+00:00",
                "source_ip": None,
                "destination_ip": None,
                "protocol": "NON_IP",
                "packet_size": 60,
            },
        ],
    )

    summary = calculate_statistics(str(db_path))

    assert summary["total_packets"] == 4
    assert summary["packets_by_protocol"] == [
        ("TCP", 2),
        ("NON_IP", 1),
        ("UDP", 1),
    ]
    assert summary["top_source_ips"] == [
        ("192.168.0.10", 2),
        ("10.0.0.5", 1),
    ]
    assert summary["top_destination_ips"] == [
        ("8.8.8.8", 2),
        ("1.1.1.1", 1),
    ]


def test_format_statistics_matches_terminal_summary_shape():
    output = format_statistics(
        {
            "total_packets": 1,
            "packets_by_protocol": [("ICMP", 1)],
            "top_source_ips": [("192.168.0.10", 1)],
            "top_destination_ips": [("8.8.8.8", 1)],
        }
    )

    assert "=== Traffic Analysis Summary ===" in output
    assert "Total packets captured: 1" in output
    assert "ICMP: 1" in output
    assert "1. 192.168.0.10 - 1 packets" in output
    assert "1. 8.8.8.8 - 1 packets" in output

