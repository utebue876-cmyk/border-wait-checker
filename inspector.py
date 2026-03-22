# inspector.py
# Tools for inspecting downloaded HTML and locating useful sections


LOG_FILE = "inspect_log.txt"


def inspect_html(raw_data):
    print("Searching page for useful lines...")

    lines = raw_data.splitlines()

    keywords = [
        "Ukraine",
        "Szacunkowy",
        "czas",
        "oczekiwania",
        "Zosin",
        "Dorohusk",
        "Hrebenne",
        "Korczowa",
        "Medyka",
        "Budomierz"
    ]

    matches = []

    for i, line in enumerate(lines):

        clean_line = line.strip()

        for keyword in keywords:
            if keyword.lower() in clean_line.lower():

                matches.append((i, keyword))
                print("Match:", keyword, "at line", i)
                break

    return matches


def show_context_to_file(raw_data, target_line, before=10, after=50):
    """
    Write a section of HTML around a line number to a text log file.
    """

    lines = raw_data.splitlines()

    start = max(0, target_line - before)
    end = min(len(lines), target_line + after + 1)

    with open(LOG_FILE, "a", encoding="utf-8") as f:

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write(f"Context around line {target_line}\n")
        f.write("=" * 60 + "\n\n")

        for i in range(start, end):
            f.write(f"{i}: {lines[i].strip()}\n")

        f.write("\n")