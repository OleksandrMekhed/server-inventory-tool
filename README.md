## Project Plan & Architecture Sketch

- **Assignment:** Server Inventory Tool
- **Course:** Programming with Python
- **Name:** Oleksandr Mekhed

---

## Server Inventory Tool

A command-line application written in Python for keeping an inventory of servers and checking whether they respond on the network.

---

## Description

**Server Inventory Tool** stores a list of servers (name, address, environment, role, status, last_checked) in a JSON file, checks them with `ping`, 
exports reports to CSV and can be used in two ways:

- as an **interactive text menu**;
- as a **CLI tool** with command-line arguments.

---


## Requirements

| Requirement | Details |
|---|---|
| Python | Tested with Python 3.14.9 |
| `ping` command | Linux, macOS, WSL or a Linux container |
| Git | Only needed if you clone the project |
| External libraries | `pytest` to run the tests and Python standard library is used |

Check your Python version:

```bash
python --version
```

---

## Getting the project

### Option A: clone with Git

```bash
git clone https://github.com/OleksandrMekhed/server-inventory-tool.git
cd server-inventory-tool
```

---

### Option B: download as ZIP

1. Open the repository page on GitHub.
2. Click **Code**, then **Download ZIP**.
3. Unpack the archive and open a terminal in the unpacked folder:

```bash
cd server-inventory-tool
```

---

### Optional: use a virtual environment

No packages need to be installed, so this step is optional. It keeps your Python setup clean:

```bash
python -m venv .venv
source .venv/bin/activate
```

---

### Install the requirements packages for the tests:

```bash
pip install -r requirements.txt
```

---

### Check that everything works

Run these commands from the project folder (the one that contains `main.py`):

```bash
python main.py --help
python main.py --list
```

If you see the help text and a table with four servers, the project is ready to use.

---

## Running the program

### Interactive menu

```bash
python main.py
```

---

### Command line (CLI)

Show all servers:

```bash
python main.py --list
```

Show servers in one environment (with or without `--list`, both work):

```bash
python main.py --list --environment prod
python main.py --environment prod
```

Check one server:

```bash
python main.py --check web01
```

Check all servers:

```bash
python main.py --check-all
```

Export a CSV report:

```bash
python main.py --export
```

Show the help text:

```bash
python main.py --help
```

---

### Arguments and exit codes

| Argument | Description | Exit code |
|---|---|---|
| `--list` | Prints all servers as a table | `0` |
| `--environment <environment>` | Prints only servers in the given environment (`dev`, `test`, `prod`). Can be combined with `--list` or used alone | `0` |
| `--check <name>` | Checks one server with ping | `0` if the server is `up`; `1` if it is `down` or not found |
| `--check-all` | Checks all servers | `0` if all are `up`; `1` if at least one is `down` |
| `--export` | Creates a CSV report in the `reports/` directory | `0` |
| `--help` | Shows the help text | `0` |
| `--verbose` | Prints extra information. The data file in use and every `ping` command that is run. Can be combined with other arguments | does not change the exit code |

The values of `--check` and `--environment` are case-insensitive: `--check WEB01` and `--environment PROD` work the same as the lowercase versions.

Inspect the exit code of the last command like this:

```bash
python main.py --check db01
echo $?
```

---

## Interactive menu

Running `python main.py` without arguments opens the menu:

| Option | Action |
|---|---|
| `1` | Show all servers |
| `2` | Show server in environment |
| `3` | Check one server |
| `4` | Check all servers |
| `5` | Export report to CSV |
| `6` | Add a server (name, address, environment and role are validated,) |
| `7` | Delete a server (servers in `prod` require typing `Y` to confirm) |
| `0` | Exit |

An invalid choice or a server name that does not exist does not end the program, a message is printed and the menu is shown again.

---

## Data storage and environment variable

By default the data is stored in `servers.json` in the folder where you run the program. Every change (add, delete, check) is saved to the file immediately.


### Using a different data file

The path to the data file is read from the `INVENTORY_DATAFILE` environment variable. Set it for a single run like this:

```bash
INVENTORY_DATAFILE=custom_servers.json python main.py --list
```

Or set it for the whole terminal session:

```bash
export INVENTORY_DATAFILE=custom_servers.json
python main.py --list
```

To go back to the default file:

```bash
unset INVENTORY_DATAFILE
```

Lookup order:

1. The `INVENTORY_DATAFILE` environment variable, if it is set.
2. The default file `servers.json`.


### Special cases

- If the data file does not exist, the program starts with an empty list and does not crash. The file is created the first time something is saved.
- If the file is corrupted or does not contain a list, it is renamed to `<filename>.bak`, a warning is printed to `stderr` and the program continues with an empty list.

---

## Project structure

```text
server-inventory-tool/
├── main.py                # entry point
├── pytest.ini             # pytest configuration (adds the project root to the import path)
├── src/
│   ├── __init__.py        # makes src a Python package
│   ├── cli.py             # command-line arguments (argparse) and exit codes
│   ├── menu.py            # interactive text menu loop
│   ├── server_action.py   # operations on the server list: find, filter, add, delete, print table
│   ├── checks.py          # server availability checks with ping (subprocess)
│   └── storage.py         # reading/writing JSON, CSV export, handling corrupted files
├── tests/
│   ├── __init__.py        # makes tests a Python package
│   ├── test_checks.py     # tests for src/checks.py
│   └── test_servers.py    # tests for src/storage.py and src/server_action.py
├── docs/
│   ├── EXPLANATION.md     # written explanation of the code
│   └── REFLECTION.md      # reflection on the choices made
├── servers.json           # saved data
├── requirements.txt       # development dependencies (pytest)
├── .gitignore
└── README.md
```

| File | Responsibility |
|---|---|
| `main.py` | Starts the program, contains `if __name__ == "__main__":` |
| `pytest.ini` | Configuration for `pytest`: `pythonpath = .` makes `from src import ...` work in the tests |
| `src/cli.py` | Defines the arguments, chooses the mode, returns exit codes |
| `src/menu.py` | Shows the menu and calls the right functions |
| `src/server_action.py` | Works with the server list in memory |
| `src/checks.py` | Runs `ping` and updates `status` and `last_checked` |
| `src/storage.py` | The only place where the program reads and writes files |
| `tests/test_checks.py` | Tests for the server checks, without using the network |
| `tests/test_servers.py` | Tests for loading and saving data, finding and filtering servers |
| `docs/EXPLANATION.md` | Written explanation of the code, with references to files and functions |
| `docs/REFLECTION.md` | Reflection on the design choices, their consequences and what would change at larger scale |
| `requirements.txt` | Packages needed only to run the tests (`pytest`) |

The program code is in the `src/` Python Package. `main.py` stays in the project root and program is started: `python main.py`. 
The data file `servers.json` and the `reports/` directory are also in the root, because their paths are relative to the folder where the program is run.


---

## Data format

Each server is a dictionary in a list:

```json
{
  "name": "web01",
  "address": "example.com",
  "environment": "prod",
  "role": "web-server",
  "status": "unknown",
  "last_checked": ""
}
```

| Field | Type | Description |
|---|---|---|
| `name` | string | Unique server name |
| `address` | string | Domain name or IP address |
| `environment` | string | `dev`, `test` or `prod` |
| `role` | string | What the server is used for |
| `status` | string | `up`, `down` or `unknown` (a new server is always `unknown`) |
| `last_checked` | string | Time of the last check as `YYYY-MM-DD HH:MM`, empty if never checked |

---

## Reports

CSV reports are saved in the `reports/` directory (created automatically). The file name contains the date and time:

```text
reports/inventory_YYYY-MM-DD_HHMM.csv
```

Example: `reports/inventory_2026-11-04_2030.csv`. The first row of the file contains the column headers.

The `reports/` directory and other generated files are excluded from the repository by `.gitignore` (`__pycache__/`, `reports/`, `.venv/`, `.idea/`, `*.bak`, `.pytest_cache/`).

---

## Limitations

- The program sends exactly one packet (`-c 1`) with a 2 second timeout (`-W 2`) through `subprocess.run()`.
- The `-W` flag means seconds on Linux but milliseconds on macOS. On macOS the timeout would therefore be 2 ms and reachable servers may wrongly show as `down`. 
Recommended environments: Linux, WSL or a Linux container.
- On Windows without WSL the `ping` flags are different, so the checks will not work.
- Some networks can block ping. In that case a server such as `example.com` is marked `down`. This is not a bug in the program.
- The address `192.0.2.10` is reserved for documentation and does not answer ping, so `test01` is always `down`.


---

## Advanced features

### Safer input

The menu does not continue with wrong values. It asks again instead.

| Situation | What happens |
|---|---|
| An empty field (name, address or role) | Message `Input cannot be empty.` and the question is asked again |
| A server name with spaces or other whitespace | Message `Server name cannot contain spaces or whitespace characters. Try again`, then asked again |
| An invalid environment | Message `Invalid environment.` and asked again until `dev`, `test` or `prod` is entered |
| A menu choice that does not exist | Message `Invalid choice.` and the menu is shown again |

The server name and the environment are converted to lowercase when entered, so `WEB01` becomes `web01` and `PROD` becomes `prod`. 
The name is handled by `ask_name`, which calls `ask_text(prompt, lowercase=True)` and the environment is handled by `ask_environment`, both in `server_action.py`. 
The address and the role are kept exactly as typed. The input is cleaned with `strip()` and `len(name.split()) > 1` detects whitespace inside a name.

**Dev Notes:**
- If a server name that does not exist is entered in "Check one server" or "Delete a server", the program says that the `Server [name] not found.` and returns to the menu.
- New server names are always saved in lowercase. If `servers.json` is edited by hand and contains a name with capital letters, the server will not be found by the lowercase name.

---

### `--verbose`

```bash
python main.py --list --verbose
```

```bash
python main.py --check db01 --verbose
```

```bash
python main.py --check-all --verbose
```

With `--verbose` the program prints the data file that is used and the exact `ping` command for every checked server. Without the flag the output is the same as before. 
The exit codes are not changed. `--verbose` outputs information directly to the standard error stream `stderr`.

---

## Running the tests

The project has automated tests written with `pytest`.


Run all tests from the project root, the folder that contains `pytest.ini`:

```bash
pytest
```

For more detailed output, with one line per test:

```bash
pytest -v
```

Run only one test file:

```bash
pytest tests/test_checks.py
```

All 12 tests should pass. They do not change `servers.json`, do not create reports in `reports/` and do not use the network.

| File | Tests | What is checked |
|---|---|---|
| `tests/test_checks.py` | 4 | `check_server` and `check_all_servers` in `src/checks.py` |
| `tests/test_servers.py` | 8 | `load_servers`, `save_servers` in `src/storage.py` and `find_server`, `filter_by_environment` in `src/server_action.py` |

The tests do not cover the functions that wait for keyboard input (`ask_text`, `ask_name`, `add_server`, `delete_server`) or the menu loop. 
These are checked by running the program by hand.

---


## Documentation

- [EXPLANATION](docs/EXPLANATION.md) - Overview of system design and code choices.
- [REFLECTION](docs/REFLECTION.md) - Insights and advanced features.