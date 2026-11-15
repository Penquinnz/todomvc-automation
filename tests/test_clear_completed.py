"""TC-TODO-027 to 028: Clear completed."""
import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, CALL_MOM, PAY_BILLS, THREE_TODOS, counter_text


@pytest.mark.P1
def test_TC_TODO_027_clear_completed_removes_only_completed_todos(todo_page):
    todo_page.add_todos(THREE_TODOS)
    todo_page.toggle(BUY_MILK)
    todo_page.toggle(CALL_MOM)

    todo_page.clear_completed()

    expect(todo_page.todo_labels).to_have_text([PAY_BILLS])
    expect(todo_page.item_counter).to_have_text(counter_text(1))
    expect(todo_page.clear_completed_button).to_be_hidden()


@pytest.mark.P2
def test_TC_TODO_028_clear_completed_shown_only_when_something_is_completed(todo_page):
    todo_page.add_todo(BUY_MILK)
    expect(todo_page.clear_completed_button).to_be_hidden()

    todo_page.toggle(BUY_MILK)

    expect(todo_page.clear_completed_button).to_be_visible()
