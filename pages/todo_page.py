"""Page Object for the React TodoMVC app.

Holds locators and user actions only. Assertions live in the tests.
Locators prefer role and accessible name, then the app's data-testid attributes.
All locators were checked against https://todomvc.com/examples/react/dist/.
"""
from playwright.sync_api import Locator, Page


class TodoPage:
    def __init__(self, page: Page):
        self.page = page
        self.new_todo_input = page.get_by_role("textbox", name="New Todo Input")
        self.main = page.get_by_test_id("main")
        self.footer = page.get_by_test_id("footer")
        self.todo_items = page.get_by_test_id("todo-item")
        self.todo_labels = page.get_by_test_id("todo-item-label")
        self.toggle_all_checkbox = page.get_by_test_id("toggle-all")
        self.edit_input = page.get_by_role("textbox", name="Edit todo")
        # The counter has no test id or accessible name; its class is part of the TodoMVC spec.
        self.item_counter = self.footer.locator(".todo-count")
        self.clear_completed_button = page.get_by_role("button", name="Clear completed")

    # ---------- navigation ----------
    def open(self, route: str = "") -> "TodoPage":
        """Open the app. route is a hash route such as "#/active"."""
        self.page.goto(f"./{route}")
        self.new_todo_input.wait_for()
        return self

    def filter_link(self, name: str) -> Locator:
        """Footer filter link: "All", "Active" or "Completed"."""
        return self.page.get_by_role("link", name=name, exact=True)

    def select_filter(self, name: str) -> None:
        self.filter_link(name).click()

    # ---------- finding items ----------
    def item(self, title: str) -> Locator:
        """The list item whose label text is exactly `title`."""
        return self.todo_items.filter(
            has=self.page.get_by_test_id("todo-item-label").get_by_text(title, exact=True)
        )

    def item_toggle(self, title: str) -> Locator:
        return self.item(title).get_by_test_id("todo-item-toggle")

    def item_delete_button(self, title: str) -> Locator:
        return self.item(title).get_by_role("button", name="Delete todo")

    # ---------- actions ----------
    def add_todo(self, title: str) -> None:
        self.new_todo_input.fill(title)
        self.new_todo_input.press("Enter")

    def add_todos(self, titles: list[str]) -> None:
        for title in titles:
            self.add_todo(title)

    def toggle(self, title: str) -> None:
        self.item_toggle(title).click()

    def toggle_all(self) -> None:
        self.toggle_all_checkbox.click()

    def delete(self, title: str) -> None:
        # The delete button is only displayed while the item is hovered.
        self.item(title).hover()
        self.item_delete_button(title).click()

    def start_editing(self, title: str) -> None:
        self.item(title).get_by_test_id("todo-item-label").dblclick()

    def edit(self, title: str, new_title: str, commit: str = "Enter") -> None:
        """Edit a todo and finish with a key ("Enter", "Escape") or "blur"."""
        self.start_editing(title)
        self.edit_input.fill(new_title)
        if commit == "blur":
            self.edit_input.blur()
        else:
            self.edit_input.press(commit)

    def clear_completed(self) -> None:
        self.clear_completed_button.click()

    def reload(self) -> None:
        self.page.reload()
        self.new_todo_input.wait_for()
