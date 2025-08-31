
# ...existing code...

# ...existing code...
from src.agents.mcp_document_agent import MCPDocumentAgent


import openai
import os

class OpenAIWorker:
    def send_chat_with_ui_update(self, user_message, chat_response_widget, model=None):
        import threading
        def run():
            loop = None
            try:
                print(f"[OpenAIWorker] Sending message: {user_message}")
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.chat(user_message, model))
                print(f"[OpenAIWorker] Received response: {response}")
            except Exception as e:
                response = f"Error: {e}"
                print(f"[OpenAIWorker] Exception: {e}")
            finally:
                if loop:
                    loop.close()
            # Update the UI widget directly (thread-safe for PyQt)
            def update_ui():
                print(f"[OpenAIWorker] Printing chat response: {response}")
                chat_response_widget.append(f"DocuPilot: {response}")
            try:
                from PyQt5.QtCore import QMetaObject, Qt
                QMetaObject.invokeMethod(chat_response_widget, "append", Qt.QueuedConnection, None, f"OpenAI: {response}")
            except Exception as ui_e:
                print(f"[OpenAIWorker] UI update exception: {ui_e}")
                update_ui()
        threading.Thread(target=run).start()
    def send_chat(self, user_message, callback, model=None):
        import threading
        def run():
            loop = None
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.chat(user_message, model))
            except Exception as e:
                response = f"Error: {e}"
            finally:
                if loop:
                    loop.close()
            callback(response)
        threading.Thread(target=run).start()

    def __init__(self, mcp_server_url="http://localhost:8000/mcp", api_key=None, model=None):
        self.mcp_agent = MCPDocumentAgent(mcp_server_url)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        print("==>>>",self.api_key)
        self.model = model or os.getenv('CUSTOM_MODEL_ID', 'gpt-3.5-turbo')
        openai.api_key = self.api_key

    async def update_excel(self, file_path, instruction):
        # Read user input and route to MCPDocumentAgent
        return await self.mcp_agent.update_document(file_path, instruction)

    async def chat(self, user_message, model=None):
        use_model = model or self.model
        # OpenAI ChatCompletion is synchronous, so run in thread for async
        import asyncio
        loop = asyncio.get_event_loop()
        def _chat():
            response = openai.ChatCompletion.create(
                model=use_model,
                messages=[{"role": "user", "content": user_message}]
            )
            return response.choices[0].message['content']
        return await loop.run_in_executor(None, _chat)
