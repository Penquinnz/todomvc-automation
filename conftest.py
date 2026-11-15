import pytest
from playwright.sync_api import Page, expect

from pages.todo_page import TodoPage

# Fail fast with a clear message instead of waiting the default 5s on every check.
expect.set_options(timeout=5_000)


@pytest.fixture
def todo_page(page: Page) -> TodoPage:
    """A fresh TodoMVC page with an empty list.

    pytest-playwright gives every test its own browser context,
    and the app keeps todos in memory only, so tests never share data.
    """
    return TodoPage(page).open()
