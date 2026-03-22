# parser.py
# ---------------------------------------------------------
# This file contains functions that:
# 1. split the downloaded HTML into lines
# 2. extract border crossing names
# 3. find a vehicle row in the HTML
# 4. extract waiting times from that row
# 5. combine crossing names with wait times
# ---------------------------------------------------------

import re


def get_lines(raw_data):
    """
    Split the raw HTML into separate lines.

    Input:
        raw_data = one big HTML string

    Output:
        list of lines
    """
    return raw_data.splitlines()


def clean_html_text(text):
    """
    Remove simple HTML tags and clean spacing.

    This is used to turn HTML like:
        <th> Dorohusk </th>

    into:
        Dorohusk
    """
    # Remove HTML tags
    text = re.sub(r"<.*?>", "", text)

    # Replace common HTML spacing
    text = text.replace("&nbsp;", " ")

    # Remove leading and trailing spaces
    text = text.strip()

    return text


def extract_crossing_names(lines):
    """
    Extract crossing names from the header row.

    We look for <th> cells that contain the border crossing names.

    Output example:
        ['Dorohusk', 'Zosin', 'Dołhobyczów', ...]
    """
    names = []

    for line in lines:
        # Only look at header cells
        if "<th" in line and "class=" in line:
            name = clean_html_text(line)

            # Ignore empty results
            if name:
                names.append(name)

    return names


def find_vehicle_block(raw_data, vehicle_keyword):
    """
    Find the HTML block for one vehicle row.

    This works by:
    1. finding the start of the vehicle row using the image file name
    2. finding the start of the next row
    3. cutting out only the current row block

    Example vehicle keywords:
        'ciezarowka.gif' = trucks
        'autobus.gif'    = buses
        'auto.gif'       = cars
    """
    # Find where this vehicle row starts
    start_index = raw_data.find(vehicle_keyword)

    # If not found, return empty string
    if start_index == -1:
        return ""

    # Move backwards to the nearest <tr before the vehicle keyword
    tr_start = raw_data.rfind("<tr", 0, start_index)

    # If no <tr found, return empty string
    if tr_start == -1:
        return ""

    # Find the next row after this one
    next_tr = raw_data.find("<tr", start_index + 1)

    # If there is no next row, use the closing </tr> of the current row
    if next_tr == -1:
        tr_end = raw_data.find("</tr>", start_index)
        if tr_end == -1:
            return ""
        return raw_data[tr_start:tr_end + len("</tr>")]

    # Otherwise return everything from this row start up to the next row
    return raw_data[tr_start:next_tr]


def extract_wait_row(raw_data, vehicle_keyword):
    """
    Extract waiting times for one vehicle type.

    Important:
    We only read the data cells that represent border crossings.
    We ignore the icon cell and description cell.

    Output example:
        ['1:00', '0:00', '0:00', '0:00', '1:00', ...]
    """
    # Get the HTML block for this vehicle row
    row_html = find_vehicle_block(raw_data, vehicle_keyword)

    # If row not found, return empty list
    if not row_html:
        return []

    # Find all data cells that hold crossing values
    data_cells = re.findall(
        r'<td[^>]*align="center"[^>]*class="dane[^"]*"[^>]*>.*?</td>',
        row_html
    )

    results = []

    for cell in data_cells:
        # Look for a normal time value like 0:00, 1:00, 10:00
        match = re.search(r"\b\d{1,2}:\d{2}\b", cell)

        if match:
            results.append(match.group())
        else:
            # Special case:
            # sometimes the page shows plain "0" instead of "0:00"
            zero_match = re.search(r">0<", cell.replace("&nbsp;", ""))

            if zero_match:
                results.append("0:00")
            else:
                # If no value exists, store N/A
                results.append("N/A")

    return results


def build_wait_table(names, times, vehicle_type):
    """
    Combine crossing names and wait times into a structured list.

    Example output:
        [
            {'vehicle': 'buses', 'crossing': 'Dorohusk', 'wait': '1:00'},
            {'vehicle': 'buses', 'crossing': 'Zosin', 'wait': '0:00'}
        ]
    """
    results = []

    # Use the smaller count so we do not crash if lengths differ
    count = min(len(names), len(times))

    for i in range(count):
        results.append({
            "vehicle": vehicle_type,
            "crossing": names[i],
            "wait": times[i]
        })

    return results