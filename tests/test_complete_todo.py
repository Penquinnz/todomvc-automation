"""TC-TODO-008 to 012: completing todos."""
import re

import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, PAY_BILLS, THREE_TODOS, counter_text

COMPLETED = re.compile(r"\bcompleted\b")


@pytest.mark.smoke
@pytest.mark.P1
def test_TC_TODO_008_mark_todo_as_completed(todo_page):
    todo_page.add_todos([BUY_MILK, PAY_BILLS])

    todo_page.toggle(BUY_MILK)

    expect(todo_page.item(BUY_MILK)).to_have_class(COMPLETED)
    expect(todo_page.item(PAY_BILLS)).not_to_have_class(COMPLETED)
    expect(todo_page.item_counter).to_have_text(counter_text(1))


@pytest.mark.P1
def test_TC_TODO_009_unmark_completed_todo(todo_page):
    todo_page.add_todos([BUY_MILK, PAY_BILLS])
    todo_page.toggle(BUY_MILK)

    todo_page.toggle(BUY_MILK)

    expect(todo_page.item(BUY_MILK)).not_to_have_class(COMPLETED)
    expect(todo_page.item_counter).to_have_text(counter_text(2))


@pytest.mark.P1
def test_TC_TODO_010_toggle_all_marks_every_todo_completed(todo_page):
    todo_page.add_todos(THREE_TODOS)

    todo_page.toggle_all()

    for title in THREE_TODOS:
        expect(todo_page.item(title)).to_have_class(COMPLETED)
    expect(todo_page.item_counter).to_have_text(counter_text(0))


@pytest.mark.P2
def test_TC_TODO_011_toggle_all_again_unmarks_every_todo(todo_page):
    todo_page.add_todos(THREE_TODOS)
    todo_page.toggle_all()

    todo_page.toggle_all()

    for title in THREE_TODOS:
        expect(todo_page.item(title)).not_to_have_class(COMPLETED)
    expect(todo_page.item_counter).to_have_text(counter_text(3))


@pytest.mark.P2
def test_TC_TODO_012_toggle_all_state_follows_individual_todos(todo_page):
    todo_page.add_todos([BUY_MILK, PAY_BILLS])

    todo_page.toggle(BUY_MILK)
    todo_page.toggle(PAY_BILLS)
    expect(todo_page.toggle_all_checkbox).to_be_checked()

    todo_page.toggle(PAY_BILLS)
    expect(todo_page.toggle_all_checkbox).not_to_be_checked()
