"""TC-TODO-021 to 026: All / Active / Completed filters."""
import re

import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, CALL_MOM, PAY_BILLS, THREE_TODOS, counter_text

SELECTED = re.compile(r"\bselected\b")


@pytest.fixture
def todos_with_one_completed(todo_page):
    """Three todos, PAY_BILLS completed."""
    todo_page.add_todos(THREE_TODOS)
    todo_page.toggle(PAY_BILLS)
    return todo_page


@pytest.mark.P1
def test_TC_TODO_021_active_filter_shows_only_active_todos(todos_with_one_completed):
    page = todos_with_one_completed

    page.select_filter("Active")

    expect(page.todo_labels).to_have_text([BUY_MILK, CALL_MOM])
    expect(page.filter_link("Active")).to_have_class(SELECTED)
    expect(page.page).to_have_url(re.compile(r"#/active$"))


@pytest.mark.P1
def test_TC_TODO_022_completed_filter_shows_only_completed_todos(todos_with_one_completed):
    page = todos_with_one_completed

    page.select_filter("Completed")

    expect(page.todo_labels).to_have_text([PAY_BILLS])
    expect(page.filter_link("Completed")).to_have_class(SELECTED)
    expect(page.page).to_have_url(re.compile(r"#/completed$"))


@pytest.mark.P2
def test_TC_TODO_023_all_filter_shows_every_todo(todos_with_one_completed):
    page = todos_with_one_completed
    page.select_filter("Active")

    page.select_filter("All")

    expect(page.todo_labels).to_have_text(THREE_TODOS)
    expect(page.filter_link("All")).to_have_class(SELECTED)


@pytest.mark.P2
def test_TC_TODO_024_open_filter_url_directly(todo_page):
    todo_page.open("#/completed")

    todo_page.add_todo(BUY_MILK)

    expect(todo_page.filter_link("Completed")).to_have_class(SELECTED)
    # A new todo is active, so the Completed view stays empty while the counter updates.
    expect(todo_page.todo_items).to_have_count(0)
    expect(todo_page.item_counter).to_have_text(counter_text(1))


@pytest.mark.P3
def test_TC_TODO_025_browser_back_returns_to_previous_filter(todos_with_one_completed):
    page = todos_with_one_completed
    page.select_filter("Active")
    page.select_filter("Completed")

    page.page.go_back()

    expect(page.filter_link("Active")).to_have_class(SELECTED)
    expect(page.todo_labels).to_have_text([BUY_MILK, CALL_MOM])


@pytest.mark.P2
def test_TC_TODO_026_completing_todo_in_active_view_removes_it_from_view(todos_with_one_completed):
    page = todos_with_one_completed
    page.select_filter("Active")

    page.toggle(BUY_MILK)

    expect(page.todo_labels).to_have_text([CALL_MOM])
    expect(page.item_counter).to_have_text(counter_text(1))
