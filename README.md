# Dad Jokes MCP Server

A lightweight Model Context Protocol (MCP) server that provides dad jokes from [icanhazdadjoke.com](https://icanhazdadjoke.com).

## Features

- 🎭 Get random dad jokes
- 🔍 Search jokes by keyword
- 🆔 Retrieve specific jokes by ID

## Tools

### `get_random_joke`
Get a random dad joke.

**Parameters:** None

**Example:**
```json
{}
```

### `search_jokes`
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

### `get_joke_by_id`
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
git clone https://github.com/your-username/dad-jokes-mcp.git
cd dad-jokes-mcp
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the server:
```bash
python server.py
```

### Testing with MCP Inspector

You can test the server locally using the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python server.py
```

## Deployment to Smithery

1. Push your code to GitHub
2. Connect your repository to [Smithery](https://smithery.ai)
3. Smithery will automatically build and deploy your MCP server

## Configuration

The server uses the following configuration:
- API: `https://icanhazdadjoke.com`
- No authentication required
- Rate limiting: Follows icanhazdadjoke.com API limits

## Credits

Dad jokes provided by [icanhazdadjoke.com](https://icanhazdadjoke.com)

## License

MIT License - see LICENSE file for details