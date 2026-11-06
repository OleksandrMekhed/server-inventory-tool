import datetime
import subprocess
import sys




def ping_server(address):
    """
    Executes the system ping command to check the availability of a specified IP address or host. Uses subprocess.run
    with a packet count limit (-c 1) and a timeout (-W 2). Catches FileNotFoundError in case the ping utility is
    missing from the system. Returns True if the ping is successful (returncode == 0) and False otherwise.
    """
    try:
        result = subprocess.run(
            ["ping", "-c", "1", "-W", "2", address],
            capture_output=True,
        )
    except FileNotFoundError:
        print("Error: 'ping' command not found.", file=sys.stderr)
        sys.exit(1)

    return result.returncode == 0




def check_server(server):
    """
    Checks the status of a specific server from the provided dictionary. Calls the ping_server function to verify the
    server address. Updates the servers status in the dictionary to "up" (available) or "down" (unavailable).
    Automatically updates the last_checked field with the current time in the format YYYY-MM-DD_HHMM.
    """
    is_up = ping_server(server["address"])

    if is_up:
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")

    return is_up




