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




