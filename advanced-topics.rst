Advanced MCP Topics
=================

This section covers advanced topics and techniques for working with the MCP Python SDK.

Server Lifecycle Management
-------------------------

Managing the lifecycle of your MCP server is crucial for resource management:

.. code-block:: python

   from contextlib import asynccontextmanager
   from collections.abc import AsyncIterator
   import aiohttp
   import aiosqlite

   from mcp.server import Server
   import mcp.types as types

   # Define a lifespan context manager
   @asynccontextmanager
   async def server_lifespan(server: Server) -> AsyncIterator[dict]:
       print("Server starting up...")
       
       # Initialize resources
       db = await aiosqlite.connect("database.db")
       session = aiohttp.ClientSession()
       
       try:
           # Yield resources to request handlers
           yield {
               "db": db,
               "session": session,
           }
       finally:
           # Clean up resources
           print("Server shutting down...")
           await session.close()
           await db.close()

   # Create server with the lifespan manager
   server = Server("advanced-server", lifespan=server_lifespan)

   # Access lifespan context in handlers
   @server.call_tool()
   async def db_query(name: str, arguments: dict) -> dict:
       # Get the database from the lifespan context
       ctx = server.request_context
       db = ctx.lifespan_context["db"]
       
       # Use the database connection
       cursor = await db.execute(arguments["query"])
       rows = await cursor.fetchall()
       return {"rows": rows}

Subscriptions and Notifications
----------------------------

MCP supports notifying clients of changes to resources and tools:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP
   import asyncio

   mcp = FastMCP("Notification Demo")

   # Track state
   messages = []

   @mcp.resource("messages://all")
   def get_messages() -> list:
       """Get all messages."""
       return messages

   @mcp.tool()
   async def add_message(content: str) -> dict:
       """Add a new message and notify subscribers."""
       message = {"id": len(messages) + 1, "content": content}
       messages.append(message)
       
       # Notify that messages resource has changed
       await mcp.notify_resource_changed("messages://all")
       
       return {"status": "added", "message": message}

   @mcp.resource("status://app")
   def get_status() -> dict:
       """Get application status."""
       return {"status": "online", "messages": len(messages)}

   # Background task to periodically notify of status changes
   async def status_updater():
       while True:
           await asyncio.sleep(30)  # Update every 30 seconds
           await mcp.notify_resource_changed("status://app")

   # Start the background task
   @mcp.on_startup
   async def startup():
       asyncio.create_task(status_updater())

WebSocket Support
--------------

In addition to the default SSE (Server-Sent Events) support, you can add WebSocket connectivity:

.. code-block:: python

   from starlette.applications import Starlette
   from starlette.routing import Mount, WebSocketRoute
   from starlette.websockets import WebSocket

   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("WebSocket Demo")

   # Define your resources, tools, and prompts here...

   # Starlette app with both SSE and WebSocket endpoints
   app = Starlette(
       routes=[
           # Mount the standard SSE endpoint
           Mount('/sse', app=mcp.sse_app()),
           
           # Custom WebSocket endpoint
           WebSocketRoute('/ws', endpoint=mcp.websocket_endpoint),
       ]
   )

   # Run with uvicorn
   import uvicorn
   
   if __name__ == "__main__":
       uvicorn.run(app, host="0.0.0.0", port=8000)

Authentication and Security
------------------------

Implementing authentication for your MCP server:

.. code-block:: python

   from starlette.applications import Starlette
   from starlette.middleware import Middleware
   from starlette.middleware.authentication import AuthenticationMiddleware
   from starlette.authentication import (
       AuthenticationBackend, AuthCredentials, BaseUser, SimpleUser
   )
   from starlette.routing import Mount
   import jwt
   
   from mcp.server.fastmcp import FastMCP

   # Create your MCP server
   mcp = FastMCP("Secure Server")

   # Define a custom authentication backend
   class JWTAuthBackend(AuthenticationBackend):
       async def authenticate(self, request):
           if "Authorization" not in request.headers:
               return None
               
           auth = request.headers["Authorization"]
           if not auth.startswith("Bearer "):
               return None
               
           token = auth.replace("Bearer ", "")
           try:
               payload = jwt.decode(
                   token, 
                   "your-secret-key",  # Use a proper secret key management in production
                   algorithms=["HS256"]
               )
               return AuthCredentials(["authenticated"]), SimpleUser(payload["sub"])
           except jwt.PyJWTError:
               return None

   # Create a Starlette app with authentication
   app = Starlette(
       routes=[
           Mount('/mcp', app=mcp.sse_app()),
       ],
       middleware=[
           Middleware(AuthenticationMiddleware, backend=JWTAuthBackend())
       ]
   )

   # Add authentication check in your handlers
   @mcp.resource("user://{id}")
   def get_user(id: str) -> dict:
       """Get user information."""
       # Access the request context
       request = mcp.get_request()
       
       # Check authentication
       if not request.user.is_authenticated:
           return {"error": "Authentication required"}
           
       if request.user.username != id and not request.user.username == "admin":
           return {"error": "Unauthorized access"}
           
       # Return user data
       return {"id": id, "name": f"User {id}"}

Streaming Responses
----------------

Handling streaming responses with MCP:

.. code-block:: python

   import asyncio
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("Streaming Demo")

   @mcp.tool()
   async def stream_data(items: int = 5, delay: float = 1.0) -> dict:
       """Demonstrate streaming data with a generator."""
       for i in range(items):
           # Yield incremental progress
           yield {
               "progress": (i + 1) / items,
               "current": i + 1,
               "total": items,
               "data": f"Item {i + 1}"
           }
           await asyncio.sleep(delay)
           
       # Final result
       return {
           "progress": 1.0,
           "message": f"Completed {items} items",
           "status": "done"
       }

Extending the Protocol
-------------------

You can extend MCP with experimental capabilities:

.. code-block:: python

   from mcp.server import Server
   from mcp.server.lowlevel import NotificationOptions
   from mcp.server.models import InitializationOptions
   import mcp.server.stdio

   # Create a server
   server = Server("extended-server")

   # Define custom experimental capability handlers
   @server.register_method("experimental/customAction")
   async def handle_custom_action(params):
       # Handle the custom action
       return {"status": "success", "result": params["value"] * 2}

   async def run():
       async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
           await server.run(
               read_stream,
               write_stream,
               InitializationOptions(
                   server_name="extended-server",
                   server_version="0.1.0",
                   capabilities=server.get_capabilities(
                       notification_options=NotificationOptions(),
                       experimental_capabilities={
                           "customAction": {}  # Define your experimental capability
                       },
                   ),
               ),
           )

Testing MCP Servers
-----------------

Strategies for testing your MCP servers:

.. code-block:: python

   import pytest
   import asyncio
   from mcp.server.fastmcp import FastMCP
   from mcp import ClientSession
   from mcp.client.socket import socket_client
   from mcp.client.stdio import stdio_client
   from mcp import StdioServerParameters

   # Server fixture for testing
   @pytest.fixture
   async def test_server():
       mcp = FastMCP("Test Server")
       
       @mcp.resource("test://data")
       def test_resource() -> str:
           return "test data"
           
       @mcp.tool()
       def test_tool(value: str) -> dict:
           return {"result": f"processed: {value}"}
           
       # Start server in background
       server_task = asyncio.create_task(mcp.run(host="localhost", port=8765))
       await asyncio.sleep(0.5)  # Wait for server to start
       
       yield mcp
       
       # Clean up
       server_task.cancel()
       await asyncio.gather(server_task, return_exceptions=True)

   # Test using socket client
   @pytest.mark.asyncio
   async def test_socket_client(test_server):
       async with socket_client({"host": "localhost", "port": 8765}) as (read, write):
           async with ClientSession(read, write) as session:
               # Initialize
               await session.initialize()
               
               # Test resource
               content, mime_type = await session.read_resource("test://data")
               assert content == "test data"
               
               # Test tool
               result = await session.call_tool("test_tool", arguments={"value": "test"})
               assert result["result"] == "processed: test"

   # Test using stdio client
   @pytest.mark.asyncio
   async def test_stdio_client():
       # Create a simple test script
       with open("test_script.py", "w") as f:
           f.write("""
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("Test Server")

   @mcp.resource("test://data")
   def test_resource() -> str:
       return "test data"

   if __name__ == "__main__":
       mcp.run(stdio=True)
   """)
       
       # Connect using stdio
       server_params = StdioServerParameters(
           command="python",
           args=["test_script.py"],
       )
       
       async with stdio_client(server_params) as (read, write):
           async with ClientSession(read, write) as session:
               await session.initialize()
               content, mime_type = await session.read_resource("test://data")
               assert content == "test data" 