import json

from src import server_action, storage




def test_load_servers_reads_valid_file(tmp_path):
    """
    Test that load_servers successfully reads and parses a valid JSON server inventory file. Test uses pytest
    tmp_path fixture to create a temporary test file. Function correctly loads data from the specified file path.
    """
    data_file = tmp_path / "servers.json"
    data = [{"name": "web01", "address": "example.com", "environment": "prod"}]
    data_file.write_text(json.dumps(data), encoding="utf-8")

    servers = storage.load_servers(data_file)

    assert len(servers) == 1
    assert servers[0]["name"] == "web01"
    assert servers[0]["environment"] == "prod"




def test_load_servers_missing_file_returns_empty_list(tmp_path):
    """
    Test that load_servers gracefully handles missing data files without crashing. Test specifies a non-existent
    file path inside a temporary directory. Function catches the missing file condition. It safely falls back and
    returns an empty list.
    """
    assert storage.load_servers(tmp_path / "missing.json") == []




def test_load_servers_corrupted_file_is_backed_up(tmp_path):
    """
    Test that load_servers safely handles corrupted JSON files by creating a backup and recovering. Test writes
    invalid JSON syntax into a temporary file. Function catches the parsing error and safely returns an empty list and
    automatically creates a backup file. Original corrupted file is cleared.
    """
    data_file = tmp_path / "servers.json"
    data_file.write_text("{{{", encoding="utf-8")

    assert storage.load_servers(data_file) == []
    assert (tmp_path / "servers.json.bak").exists()
    assert not data_file.exists()




def test_save_and_load_round_trip(tmp_path):
    """
    This test defines sample server data, serializes and writes it to a temporary file via save_servers,
    and then reads it back using load_servers. Data persistence functions correctly without data loss or corruption.
    """
    data_file = tmp_path / "servers.json"
    servers = [{"name": "db01", "address": "127.0.0.1", "environment": "prod"}]

    storage.save_servers(data_file, servers)

    assert storage.load_servers(data_file) == servers




