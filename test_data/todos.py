"""Test data shared by the tests. Change values here, not inside test logic."""

# Everyday todos used by most tests.
BUY_MILK = "Buy milk"
PAY_BILLS = "Pay bills"
CALL_MOM = "Call mom"
THREE_TODOS = [BUY_MILK, PAY_BILLS, CALL_MOM]

# Input that must not create a todo (TC-TODO-004).
BLANK_INPUTS = {
    "empty": "",
    "spaces_only": "   ",
}

# Text that must be shown exactly as typed (TC-TODO-005).
SPECIAL_TEXTS = {
    "thai": "ซื้อของเข้าบ้าน",
    "emoji": "Party time 🎉",
    "html_and_script": "<b>bold</b> & <script>alert(1)</script>",
}

LONG_TEXT = "a" * 500  # TC-TODO-006


def counter_text(active_count: int) -> str:
    """Footer counter as the live site shows it, e.g. "1 item left!".

    The trailing "!" was checked on the live site. If the wording changes,
    this is the only place to update.
    """
    noun = "item" if active_count == 1 else "items"
    return f"{active_count} {noun} left!"


# (todos to add, todos to complete, expected counter) for TC-TODO-020.
COUNTER_CASES = {
    "one_active": ([BUY_MILK], [], "1 item left!"),
    "two_active": ([BUY_MILK, PAY_BILLS], [], "2 items left!"),
    "one_of_two_done": ([BUY_MILK, PAY_BILLS], [BUY_MILK], "1 item left!"),
    "all_done": ([BUY_MILK, PAY_BILLS], [BUY_MILK, PAY_BILLS], "0 items left!"),
}
