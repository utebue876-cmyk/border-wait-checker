# reporter.py
# ---------------------------------------------------------
# This file writes the final parsed results into text files.
# We keep console output small and store useful results here.
# ---------------------------------------------------------

LOG_FILE = "border_report.txt"
DEBUG_FILE = "debug_row.txt"


def write_section(file_handle, rows, title):
    """
    Write one vehicle section to the report.

    Example:
        TRUCKS
        Dorohusk   9:00
        Zosin      0:00
    """
    file_handle.write(f"{title}\n")
    file_handle.write("\n")

    for row in rows:
        # Left align the crossing name for neat formatting
        line = f"{row['crossing']:15} {row['wait']}\n"
        file_handle.write(line)

    file_handle.write("\n")


def write_report(truck_rows, bus_rows, car_rows):
    """
    Write the full border wait report.
    """
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("Border wait times\n")
        f.write("\n")

        write_section(f, truck_rows, "TRUCKS")
        write_section(f, bus_rows, "BUSES")
        write_section(f, car_rows, "CARS")


def write_debug_row(title, row_html):
    """
    Write raw HTML for one row into a debug file.
    Useful when scraping goes wrong.
    """
    with open(DEBUG_FILE, "w", encoding="utf-8") as f:
        f.write(title + "\n\n")
        f.write(row_html)