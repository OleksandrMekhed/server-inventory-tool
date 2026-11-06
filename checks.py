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





