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
        help="Show server environment (prod, test, dev)",
    )
    pars.add_argument(
        "--check",
        metavar="NAME",
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


