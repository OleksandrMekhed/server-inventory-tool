import argparse
import sys

import checks
import menu
import storage
import server_action




def build_parser():
    """
    Command line argument parser configuration. This defines flags (--list, --environment, --list --environment, --check,
    --check-all, --export), so that the program understands exactly what the user wants it to do via the terminal.
    """
    pars = argparse.ArgumentParser(description="Server management and status checking")

    pars.add_argument(
        "--list",
        action="store_true",
        help="Show server list",
    )
    pars.add_argument(
        "--environment",
        default=None,
        type=str.lower,
        help="Show server environment (prod, test, dev)",
    )
    pars.add_argument(
        "--check",
        metavar="NAME",
        type=str.lower,
        help="Specify the name of a specific server to check",
    )
    pars.add_argument(
        "--check-all",
        action="store_true",
        help="Check all servers",
    )
    pars.add_argument(
        "--export",
        action="store_true",
        help="Export results"
    )

    return pars




def parser_cli():
    """
    The main command line controller. It reads arguments, loads the server database from a file and checks which flag
    the user has provided. Based on this, the corresponding action is triggered: displaying a list, checking a specific
    server or all servers, performing an export or opening an interactive menu.
    """
    args = build_parser().parse_args()
    file_path = storage.get_data_file_path()
    servers = storage.load_servers(file_path)

    if args.list or args.environment:
        if args.environment:
            servers = server_action.filter_by_environment(servers, args.environment)
        server_action.print_servers(servers)
        sys.exit(0)

    elif args.check:
        server = server_action.find_server(servers, name=args.check)
        if server is None:
            print(f"Server [{args.check}] not found.", file=sys.stderr)
            sys.exit(1)

        is_up = checks.check_server(server)
        storage.save_servers(file_path, servers)

        print(f"Server [{server['name']}] is {server['status']}.")
        sys.exit(0 if is_up else 1)

    elif args.check_all:
        all_up = checks.check_all_servers(servers)
        storage.save_servers(file_path, servers)
        server_action.print_servers(servers)
        sys.exit(0 if all_up else 1)

    elif args.export:
        export_path = storage.export_to_csv(servers)
        print(f"Exported successfully to: {export_path}")

    else:
        menu.show_menu(file_path, servers)
        sys.exit(0)

