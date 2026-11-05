VALID_ENVIRONMENTS = ["dev", "test", "prod"]
LINE_SEPARATOR = "-" * 110


def print_servers(servers):
    """
    Displays a list of servers in a neat table with fixed column widths. Checks if there are any servers in the list,
    displays a warning if it is empty. Formats headers and data rows using column alignment.
    """
    if not servers:
        print("No servers found.")
        return

    print(LINE_SEPARATOR)
    print(
        f"{'NAME':<15} |"
        f" {'ADDRESS':<16} |"
        f" {'ENVIRONMENT':<18} |"
        f" {'ROLE':<20} |"
        f" {'STATUS':<8} |"
        f" {'LAST CHECKED':<20}"
    )
    print(LINE_SEPARATOR)

    for server in servers:
        print(
            f"{server['name']:<15} |"
            f" {server['address']:<16} "
            f"| {server['environment']:<18} "
            f"| {server['role']:<20} "
            f"| {server['status']:<8} "
            f"| {server['last_checked']:<20}"
        )
    print(LINE_SEPARATOR)
    print()


