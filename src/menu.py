from src import checks
from src import storage
from src.server_action import (
    print_servers,
    add_server,
    delete_server,
    find_server,
    ask_environment,
    filter_by_environment,
    ask_name
)




def show_menu(file_path, servers):
    """
    show_menu(): function runs while loop for an interactive menu until the user selects the exit option (0).
    It reads the selection from the console and directs the program to the appropriate action: viewing, checking,
    adding, or exporting.
    """
    while True:
        print()
        print("=== Server Inventory Tool ===")
        print("1. Show all servers")
        print("2. Show server in environment")
        print("3. Check one server")
        print("4. Check all servers")
        print("5. Export report to CSV")
        print("6. Add a server")
        print("7. Delete a server")
        print("0. Exit")
        print()


        choice = input("Enter your choice: ").strip()


        if choice == "1":
            print_servers(servers)

        elif choice == "2":
            environment = ask_environment()
            filtered = filter_by_environment(servers, environment)
            print_servers(filtered)

        elif choice == "3":
            name = ask_name("Enter your server name: ")
            server = find_server(servers, name)
            if server is None:
                print(f"Server [{name}] not found.")
            else:
                checks.check_server(server)
                print(f"{name} - {server['status']}.")
                storage.save_servers(file_path, servers)

        elif choice == "4":
            checks.check_all_servers(servers)
            print_servers(servers)
            storage.save_servers(file_path, servers)

        elif choice == "5":
            report_path = storage.export_to_csv(servers)
            print(f"Report saved to {report_path}.")

        elif choice == "6":
            if add_server(servers):
                storage.save_servers(file_path, servers)

        elif choice == "7":
            if delete_server(servers):
                storage.save_servers(file_path, servers)

        elif choice == "0":
            print("Server Inventory Tool Stopped.")
            break

        else:
            print("Invalid choice.")

