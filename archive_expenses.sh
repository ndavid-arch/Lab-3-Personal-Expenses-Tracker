#!/bin/bash

ARCHIVE_DIR="./archives"
LOG_FILE="archive_log.txt"

# --- Function: Archive a file ---
archive_file() {
    read -p "Enter the expense file name to archive (e.g., expenses_2025-11-23.txt): " file_name

    # Check if file exists
    if [ ! -f "$file_name" ]; then
        echo "File '$file_name' does not exist."
        return
    fi

    # Create archive directory if it doesn't exist
    if [ ! -d "$ARCHIVE_DIR" ]; then
        mkdir -p "$ARCHIVE_DIR"
        echo "Created archive directory at $ARCHIVE_DIR"
    fi

    # Move file to archive
    mv "$file_name" "$ARCHIVE_DIR/"
    if [ $? -eq 0 ]; then
        echo "File '$file_name' archived successfully."

        # Log operation with timestamp
        echo "$(date '+%Y-%m-%d %H:%M:%S') - Archived: $file_name" >> "$LOG_FILE"
    else
        echo "Error: Failed to archive file '$file_name'."
    fi
}

# --- Function: Search in archive by date ---
search_archive() {
    read -p "Enter date to search for (YYYY-MM-DD): " search_date

    # Validate date format
    if [[ ! $search_date =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Invalid date format. Use YYYY-MM-DD."
        return
    fi

    file_path="$ARCHIVE_DIR/expenses_${search_date}.txt"

    if [ -f "$file_path" ]; then
        echo "Expenses for $search_date:"
        cat "$file_path"
    else
        echo "No archive file found for $search_date."
    fi
}

# --- Main menu ---
while true; do
    echo ""
    echo "-------- ARCHIVE EXPENSES --------"
    echo "1. Archive an expense file"
    echo "2. Search archived expenses by date"
    echo "3. Exit"
    echo "---------------------------------"
    read -p "Select an option (1-3): " choice

    case $choice in
        1) archive_file ;;
        2) search_archive ;;
        3) echo "Exiting script. Goodbye!"; exit 0 ;;
        *) echo "Invalid choice. Please enter 1, 2, or 3." ;;
    esac
done
