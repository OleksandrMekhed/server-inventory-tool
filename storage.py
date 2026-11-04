import csv
import datetime
import json
import os
import sys
from pathlib import Path

DEFAULT_FILENAME = "servers.json"
ENV_VAR_NAME = "INVENTORY_DATAFILE"
DEFAULT_REPORTS_DIR = "reports"
CSV_FIELDS_NAMES = ["name", "address", "environment", "role", "status", "last_checked"]




"""
get_data_file_path - determines the path to the inventory data file. It first checks for a custom path in the 
environment variables (ENV_VAR_NAME). If none is specified, it uses the default value (DEFAULT_FILENAME). 
Returns a Path object to facilitate further interaction with the file system.
"""
def get_data_file_path():
    return Path(os.environ.get(ENV_VAR_NAME, DEFAULT_FILENAME))



"""
bak_up_invalid_file - handles corrupted or invalid data files. Creates a backup of the file by appending the '.bak' 
extension to its name, outputs a warning to the standard error stream (sys.stderr) indicating the reason, and returns 
an empty list to allow the program to continue running safely.
"""
def back_up_invalid_file(path, reason):
    backup_path = path.with_name(path.name + ".bak")
    path.replace(backup_path)
    print(
        f"Warning: {path} {reason}. "
        f"Moved to {backup_path}, starting with an empty list.",
        file=sys.stderr,
    )
    return []


"""
load_servers - loads a list of servers from a JSON file. Checks if the file exists (returns an empty list if it does not). 
Performs safe reading and parsing of the JSON. Catches formatting errors JSONDecodeError and invokes a backup function. 
Verifies that the loaded data is a valid list; otherwise, it also triggers the backup.
"""
def load_servers(file_path):
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        return back_up_invalid_file(path, f"is corrupted ({error})")


    if not isinstance(data, list):
        return back_up_invalid_file(path, "does not contain a list")

    return data


"""
save_servers - saves the current list of servers back to a JSON file. Automatically creates missing parent directories 
if necessary. Writes the data with indentation indent=2 and UTF-8 support ensure_ascii=False to ensure the file is readable.
"""
def save_servers(file_path, servers):
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(
            servers,
            file,
            indent=2,
            ensure_ascii=False
        )




