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




def test_find_server():
    """
    find_server successfully locates and returns the correct server dictionary by its name, test provides a list of
    sample server dictionaries. Function correctly searches for a matching server name for example - web01 and
    returns the correct dictionary object rather than None.
    """
    servers = [
        {"name": "db01", "address": "10.0.0.5"},
        {"name": "web01", "address": "10.0.0.6"},
    ]

    result = server_action.find_server(servers, "web01")

    assert result is not None
    assert result["address"] == "10.0.0.6"




def test_find_server_not_found():
    """
    find_server gracefully handles searches for non-existent servers. Test provides a server list that does not contain
    the target name. Function checks all available records without raising errors, returns None when no matching
    server name is found.
    """
    servers = [{"name": "db01", "address": "10.0.0.5"}]

    assert server_action.find_server(servers, "test00") is None




def test_filter_by_environment():
    """
    filter_by_environment correctly returns only servers belonging to the specified environment. Test provides a list
    of servers distributed across multiple environments - prod, dev. Filtered result contains precisely the
    expected number of matching items. Every server returned in the list matches environment - prod.
    """
    servers = [
        {"name": "web01", "environment": "prod"},
        {"name": "web02", "environment": "dev"},
        {"name": "web03", "environment": "prod"},
    ]

    result = server_action.filter_by_environment(servers, "prod")

    assert len(result) == 2
    assert all(server["environment"] == "prod" for server in result)




def test_filter_by_environment_no_match():
    """
    filter_by_environment returns an empty list when no servers match the requested environment. Test specifies an
    environment - test, from the provided server list. Filtering logic handles non-matching queries safely without
    raising exceptions. An empty list is correctly returned.
    """
    servers = [{"name": "web01", "environment": "prod"}]

    assert server_action.filter_by_environment(servers, "test") == []