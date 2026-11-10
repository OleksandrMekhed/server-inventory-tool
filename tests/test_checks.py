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




