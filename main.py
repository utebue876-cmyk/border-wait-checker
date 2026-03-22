# main.py
# ---------------------------------------------------------
# Main entry point for the border wait checker.
# This version adds a first learning step:
# filter car crossings that have a valid wait time.
# ---------------------------------------------------------

from fetcher import fetch_data
from parser import (
    get_lines,
    extract_crossing_names,
    extract_wait_row,
    build_wait_table,
    find_vehicle_block,
)
from reporter import write_report, write_debug_row


def run():
    """
    Main program flow.
    """
    print("Fetching border data...")

    # Download the raw page HTML
    raw_data = fetch_data()

    # Split into lines for crossing name extraction
    lines = get_lines(raw_data)

    # Extract crossing names from the header row
    crossing_names = extract_crossing_names(lines)

    # Extract truck waiting times
    truck_times = extract_wait_row(raw_data, "ciezarowka.gif")
    truck_table = build_wait_table(crossing_names, truck_times, "trucks")

    # Extract bus waiting times
    bus_times = extract_wait_row(raw_data, "autobus.gif")
    bus_table = build_wait_table(crossing_names, bus_times, "buses")

    # Extract car waiting times
    car_times = extract_wait_row(raw_data, "auto.gif")
    car_table = build_wait_table(crossing_names, car_times, "cars")

    # Write the full report to file
    write_report(truck_table, bus_table, car_table)

    # Write raw car HTML block to debug file if needed
    car_html = find_vehicle_block(raw_data, "auto.gif")
    write_debug_row("CAR ROW HTML", car_html)

    # -----------------------------------------------------
    # LEARNING STEP 1
    # Build a new list containing only car crossings
    # where cars are allowed and a valid wait time exists.
    # -----------------------------------------------------
    valid_car_crossings = []

    for row in car_table:
        # Keep only rows where wait is not N/A
        if row["wait"] != "N/A":
            valid_car_crossings.append(row)

    # Print the filtered result to the console
    print()
    print("Valid car crossings:")
    print()

    for row in valid_car_crossings:
        print(row["crossing"], row["wait"])

    print()
    print("Report written to border_report.txt")
    print("Car row HTML written to debug_row.txt")


# Run the program
run()

