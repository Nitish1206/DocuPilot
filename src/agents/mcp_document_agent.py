

# MCPDocumentAgent routes document update requests to the MCP server using async calls.
# - update_document() calls the MCP server's update_document tool and returns the result.

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

class MCPDocumentAgent:
    def __init__(self, mcp_server_url="http://localhost:8000/mcp"):
        """
        Initialize MCPDocumentAgent.
        :param mcp_server_url: URL of the MCP server.
        """
        self.mcp_server_url = mcp_server_url

    async def update_document(self, file_path, user_command):
        """
        Update a document by calling the MCP server's update_document tool.
        :param file_path: Path to the document to update.
        :param user_command: User instruction for the update.
        :return: Tuple (success: bool, message: str)
        """
        async with streamablehttp_client(self.mcp_server_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(
                    "update_document",
                    {"file_path": file_path, "new_content": user_command}
                )
                if result.isError:
                    return False, result.content[0].text
                return True, result.content[0].text
