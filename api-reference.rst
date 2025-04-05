API Reference
============

This page provides a reference for the main classes and functions in the MCP Python SDK.

Server API
---------

FastMCP
^^^^^^

The high-level server API for quickly creating MCP servers.

.. code-block:: python

   from mcp.server.fastmcp import FastMCP

   # Create a server
   mcp = FastMCP(
       name="MyServer",             # Server name
       description="My MCP server", # Optional description
       dependencies=["pandas"],     # Optional dependencies
       lifespan=app_lifespan,       # Optional lifespan manager
   )

Methods:

- ``resource(pattern: str)`` - Decorator to register a resource handler
- ``tool()`` - Decorator to register a tool handler
- ``prompt()`` - Decorator to register a prompt handler
- ``on_startup()`` - Decorator to register a startup handler
- ``on_shutdown()`` - Decorator to register a shutdown handler
- ``run(host="localhost", port=8000, stdio=False)`` - Run the server
- ``sse_app()`` - Get the SSE ASGI application for mounting
- ``websocket_endpoint(websocket: WebSocket)`` - WebSocket endpoint for Starlette
- ``notify_resource_changed(uri: str)`` - Notify clients of a resource change
- ``notify_tools_changed()`` - Notify clients of tools list changes
- ``notify_prompts_changed()`` - Notify clients of prompts list changes
- ``get_request()`` - Get the current request (in a resource/tool/prompt handler)

Context
^^^^^^

The Context object provided to tool and resource handlers:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP, Context

   mcp = FastMCP("MyServer")

   @mcp.tool()
   async def example_tool(args: str, ctx: Context) -> str:
       # Access information and capabilities
       return "Result"

Methods:

- ``info(message: str)`` - Log an informational message
- ``warning(message: str)`` - Log a warning message
- ``error(message: str)`` - Log an error message
- ``read_resource(uri: str)`` - Read a resource
- ``report_progress(current: int, total: int)`` - Report progress of a long-running task
- ``debug(message: str)`` - Log a debug message
- ``request_id`` - Get the current request ID
- ``client_id`` - Get the client ID

Image
^^^^^

Utility class for handling image data:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP, Image
   from PIL import Image as PILImage

   mcp = FastMCP("MyServer")

   @mcp.tool()
   def create_thumbnail(image_path: str) -> Image:
       img = PILImage.open(image_path)
       img.thumbnail((100, 100))
       return Image(data=img.tobytes(), format="png")

   @mcp.tool()
   def load_image(path: str) -> Image:
       """Load an image from disk"""
       # FastMCP handles reading and format detection
       return Image(path=path)

Attributes and methods:

- ``data`` - Raw image data
- ``format`` - Image format (e.g., "png", "jpeg")
- ``mime_type`` - Mime type of the image
- ``from_pil(pil_image)`` - Create an Image from a PIL Image
- ``path`` - Source path for loading images from disk

Complex Types with Pydantic
^^^^^^^^^^^^^^^^^^^^^^^^^^

FastMCP supports complex input types using Pydantic models:

.. code-block:: python

   from pydantic import BaseModel, Field
   from typing import Annotated
   from mcp.server.fastmcp import FastMCP

   class ShrimpTank(BaseModel):
       class Shrimp(BaseModel):
           name: Annotated[str, Field(max_length=10)]

       shrimp: list[Shrimp]

   mcp = FastMCP("Shrimp Manager")

   @mcp.tool()
   def name_shrimp(
       tank: ShrimpTank,
       # Field validation in function signatures
       extra_names: Annotated[list[str], Field(max_length=10)],
   ) -> list[str]:
       """List all shrimp names in the tank"""
       return [shrimp.name for shrimp in tank.shrimp] + extra_names

Server with Lifespan
^^^^^^^^^^^^^^^^^^

Setting up servers with typed lifespan support:

.. code-block:: python

   from contextlib import asynccontextmanager
   from collections.abc import AsyncIterator
   from dataclasses import dataclass
   from mcp.server.fastmcp import FastMCP, Context

   @dataclass
   class AppContext:
       db: Database  # Your database type

   @asynccontextmanager
   async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
       """Manage application lifecycle with type-safe context"""
       # Initialize on startup
       db = await Database.connect()
       try:
           yield AppContext(db=db)
       finally:
           # Cleanup on shutdown
           await db.disconnect()

   # Pass lifespan to server
   mcp = FastMCP("My App", lifespan=app_lifespan)

   @mcp.tool()
   def query_db(ctx: Context) -> str:
       """Tool that uses initialized resources"""
       db = ctx.request_context.lifespan_context["db"]
       return db.query()

Server
^^^^^

The low-level server API for full control over the MCP server.

.. code-block:: python

   from mcp.server import Server
   import mcp.types as types

   # Create a server
   server = Server(
       name="MyServer",                 # Server name
       lifespan=my_lifespan_function,   # Optional lifespan context manager
   )

Methods:

- ``list_resources()`` - Decorator to register a list resources handler
- ``read_resource()`` - Decorator to register a read resource handler
- ``list_tools()`` - Decorator to register a list tools handler
- ``call_tool()`` - Decorator to register a call tool handler
- ``list_prompts()`` - Decorator to register a list prompts handler
- ``get_prompt()`` - Decorator to register a get prompt handler
- ``create_message()`` - Decorator to register a create message handler
- ``register_method(method: str)`` - Register a custom method handler
- ``get_capabilities(...)`` - Get server capabilities
- ``run(read_stream, write_stream, initialization_options)`` - Run the server
- ``send_notification(method: str, params: dict)`` - Send a notification to clients

Client API
---------

ClientSession
^^^^^^^^^^^

The main client class for connecting to MCP servers.

.. code-block:: python

   from mcp import ClientSession
   
   # Create a session
   async with ClientSession(
       read_stream,            # Read stream
       write_stream,           # Write stream
       sampling_callback=None, # Optional message creation callback
   ) as session:
       # Use session...

Methods:

- ``initialize()`` - Initialize the connection with the server
- ``list_resources()`` - List available resources
- ``read_resource(uri: str)`` - Read a resource
- ``subscribe_resources()`` - Subscribe to resource list changes
- ``list_tools()`` - List available tools
- ``call_tool(name: str, arguments: dict)`` - Call a tool
- ``subscribe_tools()`` - Subscribe to tool list changes
- ``list_prompts()`` - List available prompts
- ``get_prompt(name: str, arguments: dict)`` - Get a prompt
- ``subscribe_prompts()`` - Subscribe to prompt list changes
- ``create_message(params: types.CreateMessageRequestParams)`` - Create a message

Connection Functions
^^^^^^^^^^^^^^^^^

Functions for connecting to MCP servers:

.. code-block:: python

   from mcp import StdioServerParameters, SocketServerParameters
   from mcp.client.stdio import stdio_client
   from mcp.client.socket import socket_client
   
   # Connect to a server over stdio
   server_params = StdioServerParameters(
       command="python",         # Command to run
       args=["server.py"],       # Command arguments
       env=None,                 # Optional environment variables
   )
   
   async with stdio_client(server_params) as (read, write):
       # Use read and write streams...
   
   # Connect to a server over WebSocket
   server_params = SocketServerParameters(
       host="localhost",         # Server host
       port=8000,                # Server port
       ssl=False,                # SSL/TLS
   )
   
   async with socket_client(server_params) as (read, write):
       # Use read and write streams...

Type Definitions
--------------

The ``mcp.types`` module provides type definitions for MCP primitives:

.. code-block:: python

   import mcp.types as types
   
   # Resources
   resource = types.Resource(
       uri="example://resource",
       description="An example resource",
   )
   
   # Tools
   tool = types.Tool(
       name="example-tool",
       description="An example tool",
       arguments=[
           types.ToolArgument(
               name="arg1",
               description="An argument",
               required=True,
               type="string",
           )
       ]
   )
   
   # Prompts
   prompt = types.Prompt(
       name="example-prompt",
       description="An example prompt",
       arguments=[
           types.PromptArgument(
               name="arg1",
               description="An argument",
               required=True,
           )
       ]
   )
   
   # Messages
   message = types.PromptMessage(
       role="user",
       content=types.TextContent(
           type="text",
           text="Example message",
       ),
   )

Prompt Utilities
--------------

The ``mcp.server.fastmcp.prompts`` module provides utilities for creating prompt messages:

.. code-block:: python

   from mcp.server.fastmcp.prompts import base
   
   # Create message objects
   messages = [
       base.SystemMessage("You are a helpful assistant"),
       base.UserMessage("Hello, how can you help me?"),
       base.AssistantMessage("I can answer questions and help with tasks")
   ]

Command Line Interface
-------------------

The MCP CLI provides utilities for working with MCP servers:

.. code-block:: bash

   # Run the server directly
   mcp run server.py

   # Test and debug with the MCP Inspector
   mcp dev server.py

   # Install in Claude Desktop
   mcp install server.py

Development Mode Options
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Add dependencies for testing
   mcp dev server.py --with pandas --with numpy

   # Mount local code for live updates
   mcp dev server.py --with-editable .

Installation Options
^^^^^^^^^^^^^^^^^^

.. code-block:: bash

   # Custom server name
   mcp install server.py --name "My Analytics Server"

   # Environment variables (individual)
   mcp install server.py -e API_KEY=abc123 -e DB_URL=postgres://...

   # Environment variables (from file)
   mcp install server.py -f .env

   # Custom server variable
   mcp install server.py:my_custom_server

Exceptions
---------

The ``mcp.exceptions`` module provides exception classes for error handling:

.. code-block:: python

   from mcp.exceptions import (
       MCPError,                    # Base exception class
       ResourceNotFoundError,       # Resource not found
       ToolNotFoundError,           # Tool not found
       PromptNotFoundError,         # Prompt not found
       InvalidArgumentError,        # Invalid argument
       ServerError,                 # Server error
       ConnectionError,             # Connection error
       ProtocolError,               # Protocol error
   )
   
   try:
       # MCP operation
       pass
   except ResourceNotFoundError as e:
       # Handle resource not found
       pass
   except MCPError as e:
       # Handle any MCP error
       pass

Utilities
--------

The SDK includes various utility functions:

.. code-block:: python

   from mcp.utils import parse_resource_uri
   
   # Parse a resource URI pattern
   pattern = "file://{path}"
   uri = "file://example.txt"
   params = parse_resource_uri(pattern, uri)  # {"path": "example.txt"}
   
   from mcp.logging import configure_logging
   
   # Configure logging
   configure_logging(level="DEBUG")  # Set logging level

For a complete API reference, please refer to the official MCP Python SDK documentation and source code. 