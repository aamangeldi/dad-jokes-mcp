#!/usr/bin/env python3
"""
Dad Jokes MCP Server

A lightweight MCP server that provides dad jokes from icanhazdadjoke.com API.
"""

import os
import httpx
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field

# Create the MCP server instance
app = Server("dad-jokes-mcp")

# icanhazdadjoke.com API configuration
DADJOKE_API_BASE = "https://icanhazdadjoke.com"
HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Dad Jokes MCP Server (https://github.com/your-username/dad-jokes-mcp)"
}


class GetRandomJokeArgs(BaseModel):
    """Arguments for getting a random joke"""
    pass


class SearchJokesArgs(BaseModel):
    """Arguments for searching jokes"""
    term: str = Field(description="Search term to find jokes")
    limit: int = Field(default=5, description="Number of jokes to return (max 30)", ge=1, le=30)


class GetJokeByIdArgs(BaseModel):
    """Arguments for getting a specific joke by ID"""
    joke_id: str = Field(description="The ID of the joke to retrieve")


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


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="get_random_joke",
            description="Get a random dad joke from icanhazdadjoke.com",
            inputSchema=GetRandomJokeArgs.model_json_schema()
        ),
        Tool(
            name="search_jokes",
            description="Search for dad jokes by keyword or phrase",
            inputSchema=SearchJokesArgs.model_json_schema()
        ),
        Tool(
            name="get_joke_by_id",
            description="Get a specific dad joke by its ID",
            inputSchema=GetJokeByIdArgs.model_json_schema()
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls"""

    if name == "get_random_joke":
        result = await get_random_joke()
        joke_text = f"🎭 {result['joke']}\n\n(ID: {result['id']})"
        return [TextContent(type="text", text=joke_text)]

    elif name == "search_jokes":
        args = SearchJokesArgs(**arguments)
        result = await search_jokes(args.term, args.limit)

        if result['total_jokes'] == 0:
            return [TextContent(
                type="text",
                text=f"No jokes found matching '{args.term}'"
            )]

        jokes_text = f"Found {result['total_jokes']} joke(s) matching '{args.term}':\n\n"
        for i, joke in enumerate(result['results'], 1):
            jokes_text += f"{i}. {joke['joke']}\n   (ID: {joke['id']})\n\n"

        return [TextContent(type="text", text=jokes_text.strip())]

    elif name == "get_joke_by_id":
        args = GetJokeByIdArgs(**arguments)
        result = await get_joke_by_id(args.joke_id)
        joke_text = f"🎭 {result['joke']}\n\n(ID: {result['id']})"
        return [TextContent(type="text", text=joke_text)]

    else:
        raise ValueError(f"Unknown tool: {name}")


async def main():
    """Run the MCP server via HTTP"""
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.requests import Request
    from starlette.responses import Response

    port = int(os.getenv("PORT", "8081"))

    # Create SSE transport
    sse = SseServerTransport("/messages/")

    # SSE connection handler
    async def handle_sse(request: Request) -> Response:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send
        ) as streams:
            await app.run(
                streams[0],
                streams[1],
                app.create_initialization_options()
            )
        return Response()

    # Create Starlette app with CORS middleware
    from starlette.middleware.cors import CORSMiddleware

    starlette_app = Starlette(
        debug=True,
        routes=[
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=sse.handle_post_message)
        ]
    )

    # Add CORS middleware to allow Smithery to connect
    starlette_app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Run with uvicorn
    import uvicorn
    config = uvicorn.Config(
        starlette_app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
