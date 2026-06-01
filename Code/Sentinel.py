## A file that will act as a overwatcher for the type of data given by the user to make sure nothing crashes


def ask_int(prompt,min_value=None,max_value=None):



    while True:
        raw= input(prompt).strip()

        try:
            value = int(raw)
        except ValueError:
            print("Please enter a whole number.")
            continue

        if min_value is not None and value < min_value:
            print(f"Value given must be greater than {min_value}.")
            continue
        if max_value is not None and value > max_value:
            print(f"Value given must be less than {max_value}.")
            continue
        return value


def ask_float(prompt, allow_blank=False):

    while True:
        raw = input(prompt).strip()
        if raw=="" and allow_blank:
            return None
        try:
            return float(raw)
        except ValueError:
            print("  Please enter a number (or press Enter to skip).")

def ask_text(prompt, allow_blank=False):

    while True:
        text = input(prompt).strip()
        if text == "" and not allow_blank:
            print("  Please enter something.")
            continue
        return text

def ask_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("yes","y"):
            return True
        elif answer in ("no","n"):
            return False
        print("  Please answer 'y' or 'n'.")


def print_records_table(records, max_rows=20):

    if not records:
        print("No records found.")
        return

    print()
    print(f"  {'Year':<6} {'State':<22} {'Topic':<25} {'Value':<10} {'Unit'}")
    print("  " + "-" * 80)

    for r in records[:max_rows]:
        unit=(r.data_value_unit or "")[:10]
        topic=(r.topic or "")[:24]
        state=(r.state or "")[:21]
        print(f"  {r.year:<6} {state:<22} {topic:<25} "
              f"{r.data_value:<10.2f} {unit}")

    if len(records)>max_rows:
        print(f"  ... and {len(records) - max_rows} more rows")
