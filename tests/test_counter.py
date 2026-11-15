"""TC-TODO-020: the "items left" counter, one test per data set."""
import pytest
from playwright.sync_api import expect

from test_data.todos import COUNTER_CASES


@pytest.mark.P2
@pytest.mark.parametrize(
    "todos, completed, expected", COUNTER_CASES.values(), ids=COUNTER_CASES.keys()
)
def test_TC_TODO_020_counter_shows_active_count_with_correct_plural(
    todo_page, todos, completed, expected
):
    todo_page.add_todos(todos)
    for title in completed:
        todo_page.toggle(title)

    # Expected strings are written out in full on purpose,
    # so this test does not reuse the pluralisation logic it is checking.
    expect(todo_page.item_counter).to_have_text(expected)
