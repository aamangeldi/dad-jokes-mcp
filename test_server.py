#!/usr/bin/env python3
"""
Simple test script for the Dad Jokes MCP server
"""

import asyncio
import sys

# Add the current directory to the path
sys.path.insert(0, '/Users/amangeld/workplace/ai-venture-studio-hw3')

from server import get_random_joke, search_jokes, get_joke_by_id


async def test_server():
    print("🧪 Testing Dad Jokes MCP Server\n")

    # Test 1: Get a random joke
    print("Test 1: Getting a random joke...")
    try:
        joke = await get_random_joke()
        print(f"✅ Random Joke: {joke['joke']}")
        print(f"   ID: {joke['id']}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 2: Search for jokes
    print("Test 2: Searching for 'pizza' jokes...")
    try:
        results = await search_jokes("pizza", limit=3)
        print(f"✅ Found {results['total_jokes']} joke(s):")
        for i, joke in enumerate(results['results'][:3], 1):
            print(f"   {i}. {joke['joke']}")
            print(f"      ID: {joke['id']}")
        print()
    except Exception as e:
        print(f"❌ Error: {e}\n")

    # Test 3: Get a specific joke by ID
    print("Test 3: Getting joke by ID 'R7UfaahVfFd'...")
    try:
        joke = await get_joke_by_id("R7UfaahVfFd")
        print(f"✅ Joke: {joke['joke']}")
        print(f"   ID: {joke['id']}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

    print("✨ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_server())