import datetime
import subprocess
import sys




def ping_server(address, verbose=False):
    """
    Executes the system ping command to check the availability of a specified IP address or host. Uses subprocess.run
    with a packet count limit (-c 1) and a timeout (-W 2). Catches FileNotFoundError in case the ping utility is
    missing from the system. If verbose=True, prints the constructed command before execution. Returns True if the ping
    is successful (returncode == 0) and False otherwise.
    """
    command = ["ping", "-c", "1", "-W", "2", address]

    if verbose:
        print(f"Running command: {' '.join(command)}", file=sys.stderr)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
        )
    except FileNotFoundError:
        print("Error: 'ping' command not found.", file=sys.stderr)
        sys.exit(1)

    return result.returncode == 0




def check_server(server, verbose=False):
    """
    Checks the status of a specific server from the provided dictionary. Calls the ping_server function to verify the
    server address, passing the verbose parameter along. Updates the server's status in the dictionary to "up" (available)
    or "down" (unavailable). Automatically updates the last_checked field with the current time in the format YYYY-MM-DD_HHMM.
    """
    is_up = ping_server(server["address"], verbose=verbose)

    if is_up:
        server["status"] = "up"
    else:
        server["status"] = "down"

    server["last_checked"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    return is_up




def check_all_servers(servers, verbose=False):
    """
    Performs a bulk check of all servers from the inventory list. Sequentially calls check_server for each server,
    passing the verbose parameter to enable detailed command logging. Collects the check results into a list and
    uses the all() function to determine whether all servers are operational.
    """
    result = []

    for server in servers:
        result.append(check_server(server, verbose=verbose))

    return all(result)
