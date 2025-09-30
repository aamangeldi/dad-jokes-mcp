# Dad Jokes MCP Server

[![smithery badge](https://smithery.ai/badge/@aamangeldi/dad-jokes-mcp)](https://smithery.ai/server/@aamangeldi/dad-jokes-mcp)

A lightweight Model Context Protocol (MCP) server that provides dad jokes from [icanhazdadjoke.com](https://icanhazdadjoke.com).

## Features

- 🎭 Get random dad jokes
- 🔍 Search jokes by keyword
- 🆔 Retrieve specific jokes by ID
- ⚡ Fast and lightweight
- 🚀 Ready for Smithery deployment

## Tools

### `get_random_joke_tool`
Get a random dad joke.

**Example:**
```json
{}
```

### `search_jokes_tool`
Search for dad jokes containing a specific term.

**Parameters:**
- `term` (string, required): Search term to find jokes
- `limit` (integer, optional): Number of jokes to return (default: 5, max: 30)

**Example:**
```json
{
  "term": "pizza",
  "limit": 3
}
```

### `get_joke_by_id_tool`
Retrieve a specific joke by its ID.

**Parameters:**
- `joke_id` (string, required): The ID of the joke to retrieve

**Example:**
```json
{
  "joke_id": "R7UfaahVfFd"
}
```

## Local Development

### Prerequisites
- Python 3.11+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/aamangeldi/dad-jokes-mcp.git
cd dad-jokes-mcp
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install fastmcp smithery httpx
```

3. Run the server locally:
```bash
fastmcp run server.py
```

## Deployment to Smithery

1. Push your code to GitHub
2. Connect your repository to [Smithery](https://smithery.ai)
3. Smithery will automatically detect the configuration and deploy your server

The server uses:
- `runtime: python` in `smithery.yaml`
- FastMCP for the server implementation
- `@smithery.server()` decorator for configuration

## Configuration

The server requires no authentication or configuration. It uses the free icanhazdadjoke.com API with the following defaults:
- API: `https://icanhazdadjoke.com`
- No API key required
- Rate limiting follows icanhazdadjoke.com policies

## Credits

Dad jokes provided by [icanhazdadjoke.com](https://icanhazdadjoke.com)

## License

MIT License - see LICENSE file for details
