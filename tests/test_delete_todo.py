"""TC-TODO-019: deleting todos."""
import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, CALL_MOM, PAY_BILLS, THREE_TODOS, counter_text


@pytest.mark.smoke
@pytest.mark.P1
def test_TC_TODO_019_delete_todo_with_delete_button(todo_page):
    todo_page.add_todos(THREE_TODOS)

    todo_page.delete(PAY_BILLS)

    expect(todo_page.todo_labels).to_have_text([BUY_MILK, CALL_MOM])
    expect(todo_page.item_counter).to_have_text(counter_text(2))
