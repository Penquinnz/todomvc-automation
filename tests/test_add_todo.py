"""TC-TODO-001 to 007: adding todos."""
import pytest
from playwright.sync_api import expect

from test_data.todos import (BLANK_INPUTS, BUY_MILK, LONG_TEXT, SPECIAL_TEXTS,
                             THREE_TODOS, counter_text)


@pytest.mark.smoke
@pytest.mark.P1
def test_TC_TODO_001_add_single_todo(todo_page):
    todo_page.add_todo(BUY_MILK)

    expect(todo_page.todo_labels).to_have_text([BUY_MILK])
    expect(todo_page.item_counter).to_have_text(counter_text(1))
    expect(todo_page.new_todo_input).to_have_value("")


@pytest.mark.P1
def test_TC_TODO_002_add_multiple_todos_keeps_order(todo_page):
    todo_page.add_todos(THREE_TODOS)

    expect(todo_page.todo_labels).to_have_text(THREE_TODOS)
    expect(todo_page.item_counter).to_have_text(counter_text(3))


@pytest.mark.P2
def test_TC_TODO_003_add_todo_trims_leading_and_trailing_spaces(todo_page):
    todo_page.add_todo(f"   {BUY_MILK}   ")

    expect(todo_page.todo_labels).to_have_text([BUY_MILK])


@pytest.mark.P2
@pytest.mark.parametrize("text", BLANK_INPUTS.values(), ids=BLANK_INPUTS.keys())
def test_TC_TODO_004_blank_input_does_not_add_todo(todo_page, text):
    todo_page.add_todo(text)

    expect(todo_page.todo_items).to_have_count(0)
    expect(todo_page.main).to_be_hidden()


@pytest.mark.P2
@pytest.mark.parametrize("text", SPECIAL_TEXTS.values(), ids=SPECIAL_TEXTS.keys())
def test_TC_TODO_005_special_text_is_shown_as_plain_text(todo_page, text):
    todo_page.add_todo(text)

    expect(todo_page.todo_labels).to_have_text([text])
    # Markup must be shown as text, never rendered as HTML elements.
    expect(todo_page.todo_labels.locator("b, script")).to_have_count(0)


@pytest.mark.P3
def test_TC_TODO_006_add_very_long_todo(todo_page):
    todo_page.add_todo(LONG_TEXT)

    expect(todo_page.todo_labels).to_have_text([LONG_TEXT])


@pytest.mark.P2
def test_TC_TODO_007_main_and_footer_appear_only_when_list_has_todos(todo_page):
    expect(todo_page.main).to_be_hidden()
    expect(todo_page.footer).to_be_hidden()

    todo_page.add_todo(BUY_MILK)

    expect(todo_page.main).to_be_visible()
    expect(todo_page.footer).to_be_visible()
