import re

from src import checks

TIME_FORMAT = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}"




def test_check_server_marks_down_and_sets_time(monkeypatch):
    """
    Test that check_server correctly handles a failed server ping. ping_server function to simulate a network failure - returning False.
    Function returns False indicating failure, the server dictionary status is updated to 'down'. Formatted timestamp matching
    YYYY-MM-DD HH:MM is saved in last_checked.
    """
    monkeypatch.setattr(checks, "ping_server", lambda address, verbose=False: False)
    server = {"address": "192.0.2.10", "status": "unknown", "last_checked": ""}

    result = checks.check_server(server)

    assert result is False
    assert server["status"] == "down"
    assert re.fullmatch(TIME_FORMAT, server["last_checked"])




def test_check_server_marks_up(monkeypatch):
    """
    Test that check_server correctly handles a successful server ping. ping_server function to simulate a successful
    connection - returning True. Function returns True indicating success, server dictionary status is updated to 'up'.
    Formatted timestamp matching YYYY-MM-DD HH:MM is saved in last_checked.
    """
    monkeypatch.setattr(checks, "ping_server", lambda address, verbose=False: True)
    server = {"address": "192.0.2.1", "status": "unknown", "last_checked": ""}

    result = checks.check_server(server, verbose=False)

    assert result is True
    assert server["status"] == "up"
    assert re.fullmatch(TIME_FORMAT, server["last_checked"])




def test_check_all_servers_all_up(monkeypatch):
    """
    Test that check_all_servers correctly handles a batch check where all servers are operational. ping_server to
    consistently return True for any address. Function iterates through all servers in the inventory list, each server
    status is successfully updated to 'up'. Function returns True because every individual check passed.
    """
    monkeypatch.setattr(checks, "ping_server", lambda address, verbose=False: True)
    servers = [
        {"name": "web01", "address": "192.0.2.1", "status": "unknown"},
        {"name": "web02", "address": "192.0.2.2", "status": "unknown"},
    ]

    result = checks.check_all_servers(servers, verbose=False)

    assert result is True
    assert all(server["status"] == "up" for server in servers)




def test_check_all_servers_down(monkeypatch):
    """
    Test that check_all_servers correctly handles a batch check where one or more servers fail. This test uses an
    iterator to mock ping_server, returning True for the first server and False for the second server sequentially.
    Function checks all target servers regardless of individual failures. Individual server statuses are updated
    accurately - 'up' for the first, 'down' for the second. Function returns False, indicating that the bulk
    check was not fully successful.
    """
    answers = iter([True, False])
    monkeypatch.setattr(
        checks, "ping_server", lambda address, verbose=False: next(answers)
    )
    servers = [
        {"name": "web01", "address": "192.0.2.1", "status": "unknown"},
        {"name": "web02", "address": "192.0.2.2", "status": "unknown"},
    ]

    result = checks.check_all_servers(servers, verbose=False)

    assert result is False
    assert servers[0]["status"] == "up"
    assert servers[1]["status"] == "down"