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




def find_server(servers, name):
    """
    Searches for a server in the list by its name.  Returns the found server dictionary, or None if the server is not found.
    """
    for server in servers:
        if server["name"] == name:
            return server
    return None




def filter_by_environment(servers, environment):
    """
    Filters the list of servers by the specified environment - 'dev', 'prod' or 'test'. Returns a new list containing
    only the servers with the matching environment.
    """
    new_servers = []
    for server in servers:
        if server["environment"] == environment:
            new_servers.append(server)
    return new_servers




def ask_environment():
    """
    Interactively prompts the user for the environment and validates their input. Runs in a loop until the user enters
    one of the allowed values from VALID_ENVIRONMENTS.
    """
    while True:
        env = input("Enter environment (dev/test/prod): ").strip().lower()
        if env in VALID_ENVIRONMENTS:
            return env
        else:
            print("Invalid environment.")




def ask_text(prompt, lowercase=False):
    """
    ask_text() function ask the user for text and if necessary, convert it to lowercase.
    """
    while True:
        text = input(prompt).strip()
        if text:
            return text.lower() if lowercase else text

        print("Input cannot be empty.")




def ask_name(prompt):
    """
    ask_name() function check the name for the presence of any whitespace characters, including tabs using
    len(name.split()) > 1, this is more reliable than a simple search using `in`.
    """
    while True:
        name = ask_text(prompt, lowercase=True)
        if len(name.split()) > 1:
            print("Server name cannot contain spaces or whitespace characters. Try again.")
            continue
        return name




def add_server(servers):
    """
    Adds a new server to the master list, checking for name uniqueness. Prompts for the name via ask_name, address
    via ask_text, environment via ask_environment and role via ask_text. Sets the initial status to 'unknown' and
    the check time to empty. Adds the object to the list and returns True upon success.
    """
    name = ask_name("Enter server name: ")

    if find_server(servers, name) is not None:
        print(f"Server [{name}] already exists.")
        return False

    address = ask_text("Enter server address: ")
    environment = ask_environment()
    role = ask_text("Enter server role: ")

    server = {
        "name": name,
        "address": address,
        "environment": environment,
        "role": role,
        "status": "unknown",
        "last_checked": ""
    }
    servers.append(server)
    print(f"Server [{name}] added.")
    return True




def delete_server(servers):
    """
    Removes a server from the list by prompt name via ask_name with additional safeguards. Verifies the existence of
    the server. If the server environment is 'prod', it requires explicit confirmation by entering 'Y', to prevent
    the accidental deletion of critical production infrastructure.
    """
    name = ask_name("Enter server name: ")

    server = find_server(servers, name)
    if server is None:
        print(f"Server [{name}] not found.")
        return False

    if server["environment"] == "prod":
        answer = input("Server in environment - [prod]! Enter [y] to confirm delete: ").strip().lower()
        if answer != "y":
            print("Deletion cancelled.")
            return False

    servers.remove(server)
    print(f"Server [{name}] removed.")
    return True