import sqlite3

from app.storage import initialize_database, insert_packets


def test_initialize_database_creates_packets_schema(tmp_path):
    db_path = tmp_path / "traffic.db"

    initialize_database(str(db_path))

    with sqlite3.connect(db_path) as connection:
        columns = connection.execute("PRAGMA table_info(packets)").fetchall()

    assert [column[1] for column in columns] == [
        "id",
        "captured_at",
        "source_ip",
        "destination_ip",
        "protocol",
        "packet_size",
    ]


def test_insert_packets_saves_packet_records(tmp_path):
    db_path = tmp_path / "traffic.db"
    initialize_database(str(db_path))

    insert_packets(
        str(db_path),
        [
            {
                "captured_at": "2026-06-16T18:00:00+00:00",
                "source_ip": "192.168.0.10",
                "destination_ip": "8.8.8.8",
                "protocol": "UDP",
                "packet_size": 128,
            }
        ],
    )

    with sqlite3.connect(db_path) as connection:
        row = connection.execute(
            """
            SELECT captured_at, source_ip, destination_ip, protocol, packet_size
            FROM packets
            """
        ).fetchone()

    assert row == (
        "2026-06-16T18:00:00+00:00",
        "192.168.0.10",
        "8.8.8.8",
        "UDP",
        128,
    )

