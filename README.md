# Expenses Tracker Application

A simple command-line Python application for managing personal expenses, tracking balances, and archiving past records using a Bash script.

## Project Overview

The Expenses Tracker allows a user to:

* Add expenses with automatic validation
* Track remaining balance (including controlled overspending)
* View all expenses in a clean report
* Archive old expense records using a dedicated shell script
* Log all archival activity for auditing

## Project Structure

* expenses-tracker.py      # Main Python application
* archive_expenses.sh      # Shell script for archiving old expenses
* balance.txt              # Stores starting balance and updated balance
* archives/                # Automatically created folder for archived files

  * YYYY-MM-DD/            # Daily archive folders created by the script
* archive_log.txt          # Log of archival operations

## Features

### Python Application (expenses-tracker.py)

* Add new expenses with validation (amount, category, description).
* Deduct expenses from balance.
* Allow negative “available balance” when overspending.
* Always show:

  * Initial Balance
  * Total Expenses
  * Available Balance (can go negative)
* Display all expenses in table format.
* Save all information into text files (persistent storage).

### Archival Shell Script (archive_expenses.sh)

The script:

1. Checks if an `archives/` directory exists — if not, creates it.
2. Creates a subfolder based on today’s date (`YYYY-MM-DD`).
3. Moves `balance.txt` and any generated expense file into the archive folder.
4. Logs the operation (with timestamp) in `archive_log.txt`.
5. Accepts a date argument (`YYYY-MM-DD`) to retrieve archived files and print them to the terminal.

## Installation & Setup

### Requirements

* Python 3 installed
* Bash shell (Linux/macOS or Git Bash on Windows)

### Run the application

```bash
python3 expenses-tracker.py
```

### Archive your files

```bash
chmod +x archive_expenses.sh
./archive_expenses.sh
```

## Testing Instructions

* Test the Python program on multiple systems (Windows Git Bash, macOS, Linux).
* Ensure file paths are correct when moving files.
* Run the archive script multiple times to verify:

  * logs are updated
  * folders are created correctly
  * archived files can be retrieved
* Verify input validation in the Python program.

## Key Evaluation Items

### Validation

* Proper file names and folder structure
* Correct data types and input handling
* Proper path usage for file operations

### Functionality

* Working archival process
* Logging with timestamps
* Expense calculations and reporting

## Author

Ntwali Beni David
African Leadership University – Year 1, T2


