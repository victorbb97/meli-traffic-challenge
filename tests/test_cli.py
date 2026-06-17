from app.cli import build_parser


def test_cli_defaults():
    parser = build_parser()

    args = parser.parse_args([])

    assert args.interface is None
    assert args.timeout == 60
    assert args.count == 100
    assert args.db_path == "traffic.db"
    assert args.pcap_file is None


def test_cli_accepts_offline_pcap_file():
    parser = build_parser()

    args = parser.parse_args(
        [
            "--interface",
            "eth0",
            "--timeout",
            "10",
            "--count",
            "5",
            "--db-path",
            "data/test.db",
            "--pcap-file",
            "samples/capture.pcap",
        ]
    )

    assert args.interface == "eth0"
    assert args.timeout == 10
    assert args.count == 5
    assert args.db_path == "data/test.db"
    assert args.pcap_file == "samples/capture.pcap"


def test_cli_accepts_live_capture_arguments():
    parser = build_parser()

    args = parser.parse_args(
        [
            "--interface",
            "eth0",
            "--timeout",
            "30",
            "--count",
            "50",
            "--db-path",
            "traffic.db",
        ]
    )

    assert args.interface == "eth0"
    assert args.timeout == 30
    assert args.count == 50
    assert args.db_path == "traffic.db"
    assert args.pcap_file is None
