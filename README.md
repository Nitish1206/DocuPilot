src/
  actions/
  agents/
  app/
  designer/
  utils/
```

# SOCR Documentation Editor

This project is a documentation editor for the SOCR_AI platform. It provides tools and interfaces for creating, editing, and managing documentation within the SOCR ecosystem, with AI-powered document updates and chat support.

## Features

- **Document Update via MCP Server**: All document modifications are routed through a Python MCP server, which exposes an `update_document` tool for secure and standardized updates.
- **OpenAI Chat Support**: Integrated OpenAI chat for user assistance and natural language interaction.
- **Async Workflow**: Document updates and chat interactions are handled asynchronously for responsive UI and robust error handling.
- **Modular Agents and Workers**: The codebase uses a modular structure with agents for document operations and workers for chat and routing.

## Project Structure

```
src/
  actions/    # Action handlers and logic
  agents/     # MCPDocumentAgent and other agent modules
  app/        # Main application logic and entry points
  designer/   # UI/UX design components and resources
  utils/      # Utility functions and helpers (OpenAIWorker, etc.)
```

## Getting Started

1. Clone the repository.
2. Install Python dependencies:
   ```powershell
   pip install "mcp[cli]" openai pandas python-docx python-dotenv
   ```
3. Set up your `.env` file with your OpenAI API key and model ID:
   ```env
   OPENAI_API_KEY=your_openai_key
   CUSTOM_MODEL_ID=gpt-3.5-turbo
   ```
4. Start the MCP server (see `mcp_server.py` example below).
5. Run the documentation editor application.

## MCP Server Example

Create a file `mcp_server.py`:
```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Document Update Server")

@mcp.tool()
def update_document(file_path: str, new_content: str) -> str:
  """Update a document with new content."""
  try:
    with open(file_path, "w", encoding="utf-8") as f:
      f.write(new_content)
    return f"Document {file_path} updated successfully."
  except Exception as e:
    return f"Error updating document: {e}"

if __name__ == "__main__":
  mcp.run(transport="streamable-http")
```

## Usage

Run the MCP server:
```powershell
python mcp_server.py
```

Run the documentation editor (see main.py):
```powershell
python main.py
```


## Contributing

Contributions are welcome! Please submit issues or pull requests for improvements or bug fixes.

## License

This project is licensed under the MIT License.
