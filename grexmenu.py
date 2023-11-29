from textual.reactive import reactive
from textual.app import App, ComposeResult, RenderResult
from textual.containers import Grid
from textual.widgets import Static, Footer, Header, ListView, ListItem, Label, Button, Input
from textual.screen import ModalScreen
from textual.widget import Widget
from textual import events

TEXT = """\
This is the primary section where the selected application will run.

"""

class QuitScreen(ModalScreen):
    """Screen with a dialog to quit."""

    def compose(self) -> ComposeResult:
        yield Grid(
            Label("Are you sure you want to quit?", id="question"),
            Button("Quit", variant="error", id="quit"),
            Button("Cancel", variant="primary", id="cancel"),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "quit":
            self.app.exit()
        else:
            self.app.pop_screen()

class Messenger(Widget):
    '''tests messaging and refresh display with reactive'''
    message = reactive("No message yet")

    def render(self) -> str:
        return f"Message: {self.message}"
    
# create a ListView for sidebar menu
class Menu(Static):
    """A ListView that displays a list of items."""
    def compose(self) -> ComposeResult:
        yield ListView (
                ListItem(Label("One")),
                ListItem(Label("Two")),
                ListItem(Label("Three")),
                ListItem(Label("Four")),
                ListItem(Label("Five")),
            )



class Messenger(Widget):
    '''tests messaging and refresh display with reactive'''
    message = reactive("No message yet")

    def render(self) -> str:
        return f"Message: {self.message}"

class grexmenu(App):
    CSS_PATH = "grexmenu.tcss"
    BINDINGS = [("q", "request_quit", "Quit"), ("1", "select_1", "Select 1"), ("2", "select_2", "Select 2"), 
                ("3", "select_3", "Select 3"), ("4", "select_4", "Select 4"), ("5", "select_5", "Select 5")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Menu(id="sidebar")
        yield Static(id="body")
        yield Input(placeholder="Enter a message", id="input")
        yield Messenger()
        yield Footer()

    # Testing reactive events with binding keys
    def action_select_1(self) -> None:
        self.query_one(Messenger).message = "One"
    
    def action_select_2(self) -> None:
        self.query_one(Messenger).message = "Two"

    def action_select_3(self) -> None:
        self.query_one(Messenger).message = "Three"

    def action_select_4(self) -> None:
        self.query_one(Messenger).message = "Four"

    def action_select_5(self) -> None:
        self.query_one(Messenger).message = "Five"

    # testing reactive events with input
    def on_input_changed(self, event: Input.Changed) -> None:
        self.query_one(Messenger).message = event.value

    # launch exit modal screen with q
    def action_request_quit(self) -> None:
        """Action to display the quit dialog."""
        self.push_screen(QuitScreen())

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle a selection event."""
        self.query_one(Messenger).message = event.list_view.index


if __name__ == "__main__":
    app = grexmenu()
    app.run()