from src.utils.openai_worker import OpenAIWorker

class ChatAction:
    def __init__(self, chat_response_widget):
        self.worker = OpenAIWorker()
        self.chat_response_widget = chat_response_widget

    def handle_send(self, user_message):
        if user_message:
            self.chat_response_widget.append(f"You: {user_message}")
            self.worker.send_chat_with_ui_update(user_message, self.chat_response_widget)
