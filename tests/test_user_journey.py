"""TC-TODO-030: end-to-end user journey across features."""
import re

import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, CALL_MOM, PAY_BILLS, THREE_TODOS, counter_text

COMPLETED = re.compile(r"\bcompleted\b")


@pytest.mark.smoke
@pytest.mark.P1
def test_TC_TODO_030_plan_day_complete_and_clean_up(todo_page):
    todo_page.add_todos(THREE_TODOS)
    expect(todo_page.item_counter).to_have_text(counter_text(3))

    todo_page.toggle(BUY_MILK)
    todo_page.edit(CALL_MOM, "Call mom tonight")
    expect(todo_page.item(BUY_MILK)).to_have_class(COMPLETED)
    expect(todo_page.item_counter).to_have_text(counter_text(2))

    todo_page.select_filter("Active")
    expect(todo_page.todo_labels).to_have_text([PAY_BILLS, "Call mom tonight"])

    todo_page.select_filter("All")
    todo_page.clear_completed()
    expect(todo_page.todo_labels).to_have_text([PAY_BILLS, "Call mom tonight"])
    expect(todo_page.clear_completed_button).to_be_hidden()
