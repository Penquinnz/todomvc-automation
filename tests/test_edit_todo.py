"""TC-TODO-013 to 018: editing todos."""
import pytest
from playwright.sync_api import expect

from test_data.todos import BUY_MILK, PAY_BILLS, counter_text

NEW_TITLE = "Buy oat milk"


@pytest.mark.smoke
@pytest.mark.P1
def test_TC_TODO_013_edit_todo_and_save_with_enter(todo_page):
    todo_page.add_todo(BUY_MILK)

    todo_page.edit(BUY_MILK, NEW_TITLE, commit="Enter")

    expect(todo_page.todo_labels).to_have_text([NEW_TITLE])
    expect(todo_page.edit_input).to_be_hidden()


@pytest.mark.P2
def test_TC_TODO_014_edit_todo_and_save_on_blur(todo_page):
    todo_page.add_todo(BUY_MILK)

    todo_page.edit(BUY_MILK, NEW_TITLE, commit="blur")

    expect(todo_page.todo_labels).to_have_text([NEW_TITLE])
    expect(todo_page.edit_input).to_be_hidden()


@pytest.mark.P2
@pytest.mark.parametrize("blank", ["", "   "], ids=["empty", "spaces_only"])
def test_TC_TODO_015_edit_to_blank_deletes_todo(todo_page, blank):
    todo_page.add_todos([BUY_MILK, PAY_BILLS])

    todo_page.edit(BUY_MILK, blank, commit="Enter")

    expect(todo_page.todo_labels).to_have_text([PAY_BILLS])
    expect(todo_page.item_counter).to_have_text(counter_text(1))


@pytest.mark.P3
def test_TC_TODO_016_edit_trims_leading_and_trailing_spaces(todo_page):
    todo_page.add_todo(BUY_MILK)

    todo_page.edit(BUY_MILK, f"   {NEW_TITLE}   ", commit="Enter")

    expect(todo_page.todo_labels).to_have_text([NEW_TITLE])


@pytest.mark.P2
@pytest.mark.known_defect
@pytest.mark.xfail(
    raises=AssertionError,
    reason="Known defect: Escape does not cancel editing (TodoMVC spec requires it). "
           "The typed text is then saved on blur, so the original title is lost.",
)
def test_TC_TODO_017_escape_cancels_edit_and_keeps_original_title(todo_page):
    todo_page.add_todo(BUY_MILK)

    todo_page.edit(BUY_MILK, NEW_TITLE, commit="Escape")

    expect(todo_page.edit_input).to_be_hidden()
    expect(todo_page.todo_labels).to_have_text([BUY_MILK])


@pytest.mark.P3
def test_TC_TODO_018_editing_hides_toggle_and_delete_controls(todo_page):
    todo_page.add_todo(BUY_MILK)

    todo_page.start_editing(BUY_MILK)

    expect(todo_page.edit_input).to_be_visible()
    expect(todo_page.edit_input).to_have_value(BUY_MILK)
    expect(todo_page.item_toggle(BUY_MILK)).to_be_hidden()
    expect(todo_page.item_delete_button(BUY_MILK)).to_be_hidden()
