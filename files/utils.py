"""
utils.py
--------
Small helper functions used across the program.
Mostly safe wrappers around input() so the menu doesn't crash
when the user types something unexpected.
"""


def ask_int(prompt, min_value=None, max_value=None):
    """
    Keeps asking until the user enters a valid integer.
    Optionally enforces minimum and maximum bounds.
    """
    while True:
        raw = input(prompt).strip()
        try:
            value = int(raw)
        except ValueError:
            print("  Please enter a whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"  Value must be at least {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"  Value must be at most {max_value}.")
            continue
        return value


def ask_float(prompt, allow_blank=False):
    """
    Keeps asking until the user enters a valid number.
    If allow_blank=True, returns None when the user just presses Enter.
    """
    while True:
        raw = input(prompt).strip()
        if raw == "" and allow_blank:
            return None
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number (or press Enter to skip).")


def ask_text(prompt, allow_blank=False):
    """Asks for a text answer. Empty strings rejected unless allow_blank=True."""
    while True:
        text = input(prompt).strip()
        if text == "" and not allow_blank:
            print("  Please enter something.")
            continue
        return text


def ask_yes_no(prompt):
    """Returns True for yes, False for no. Accepts y / yes / n / no."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please answer with 'y' or 'n'.")


def print_records_table(records, max_rows=20):
    """Prints a simple table of records to the terminal."""
    if not records:
        print("  No records to display.")
        return

    print()
    print(f"  {'Year':<6} {'State':<22} {'Topic':<25} {'Value':<10} {'Unit'}")
    print("  " + "-" * 80)

    for r in records[:max_rows]:
        unit = (r.data_value_unit or "")[:10]
        topic = (r.topic or "")[:24]
        state = (r.state or "")[:21]
        print(f"  {r.year:<6} {state:<22} {topic:<25} "
              f"{r.data_value:<10.2f} {unit}")

    if len(records) > max_rows:
        print(f"  ... and {len(records) - max_rows} more rows")
