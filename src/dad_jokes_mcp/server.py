"""
Dad Jokes MCP Server

A lightweight MCP server that provides dad jokes from icanhazdadjoke.com API.
"""

import httpx
from mcp.server.fastmcp import FastMCP
from smithery.decorators import smithery

# icanhazdadjoke.com API configuration
DADJOKE_API_BASE = "https://icanhazdadjoke.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Dad Jokes MCP Server (https://github.com/aamangeldi/dad-jokes-mcp)"
}


async def get_random_joke() -> dict:
    """Fetch a random dad joke"""
    async with httpx.AsyncClient() as client:
        response = await client.get(DADJOKE_API_BASE, headers=HEADERS)
        response.raise_for_status()
        return response.json()


async def search_jokes(term: str, limit: int = 5) -> dict:
    """Search for jokes containing a term"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DADJOKE_API_BASE}/search",
            headers=HEADERS,
            params={"term": term, "limit": limit}
        )
        response.raise_for_status()
        return response.json()


async def get_joke_by_id(joke_id: str) -> dict:
    """Get a specific joke by its ID"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{DADJOKE_API_BASE}/j/{joke_id}",
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()


@smithery.server()
def create_server():
    """Create and configure the FastMCP server"""
    mcp = FastMCP("dad-jokes-mcp")

    @mcp.tool()
    async def get_random_joke_tool() -> str:
        """Get a random dad joke from icanhazdadjoke.com"""
        result = await get_random_joke()
        return f"{result['joke']}\n\n(ID: {result['id']})"

    @mcp.tool()
    async def search_jokes_tool(
        term: str,
        limit: int = 5
    ) -> str:
        """
        Search for dad jokes by keyword or phrase.

        Args:
            term: Search term to find jokes
            limit: Number of jokes to return (default: 5, max: 30)
        """
        if limit < 1 or limit > 30:
            limit = min(max(limit, 1), 30)

        result = await search_jokes(term, limit)

        if result['total_jokes'] == 0:
            return f"No jokes found matching '{term}'"

        jokes_text = f"Found {result['total_jokes']} joke(s) matching '{term}':\n\n"
        for i, joke in enumerate(result['results'], 1):
            jokes_text += f"{i}. {joke['joke']}\n   (ID: {joke['id']})\n\n"

        return jokes_text.strip()

    @mcp.tool()
    async def get_joke_by_id_tool(joke_id: str) -> str:
        """
        Get a specific dad joke by its ID.

        Args:
            joke_id: The ID of the joke to retrieve
        """
        result = await get_joke_by_id(joke_id)
        return f"{result['joke']}\n\n(ID: {result['id']})"

    return mcp