
# ...existing code...

# ...existing code...
from src.agents.mcp_document_agent import MCPDocumentAgent


import openai
import os

class OpenAIWorker:
    def __init__(self, mcp_server_url="http://localhost:8000/mcp", api_key=None, model=None):
        self.mcp_agent = MCPDocumentAgent(mcp_server_url)
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
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
