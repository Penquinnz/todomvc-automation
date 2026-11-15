"""TC-TODO-029: todos survive a page reload (TodoMVC spec: localStorage)."""
import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, PAY_BILLS


@pytest.mark.P2
@pytest.mark.known_defect
@pytest.mark.xfail(
    raises=AssertionError,
    reason="Known defect: the React example keeps todos in memory only, "
           "so a reload empties the list. The TodoMVC spec requires persistence.",
)
def test_TC_TODO_029_todos_persist_after_reload(todo_page):
    todo_page.add_todos([BUY_MILK, PAY_BILLS])
    todo_page.toggle(BUY_MILK)

    todo_page.reload()

    expect(todo_page.todo_labels).to_have_text([BUY_MILK, PAY_BILLS])
