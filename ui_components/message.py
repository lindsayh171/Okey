import arcade.gui

class Message:
    def __init__(self, manager, text):
        self.manager = manager
        self.text = text

    def show(self):
        message_box = arcade.gui.UIMessageBox(
            width=300,
            height=200,
            message_text=self.text,
            buttons=["Ok"]
        )

        self.manager.add(message_box)