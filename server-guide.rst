Building MCP Servers
=================

This guide covers how to build MCP servers using the Python SDK. We'll explore server setup, resources, tools, prompts, and other important features.

Server Types
----------

The MCP Python SDK provides two main ways to create servers:

1. **FastMCP**: A high-level API for quickly creating servers with minimal boilerplate
2. **Server**: A low-level API for more control over the server lifecycle

FastMCP was originally a separate project but has now been integrated into the official MCP Python SDK. It offers a Pythonic, high-level interface that's ideal for most use cases.

Using FastMCP
-----------

FastMCP is the recommended way to create MCP servers for most use cases:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP

   # Create a server with a name
   mcp = FastMCP("My Application")

   # Specify dependencies for deployment and development
   mcp = FastMCP("My Application", dependencies=["pandas", "numpy"])

   # Start the server
   mcp.run()  # Defaults to localhost:8000

A simple "Hello World" example:

.. code-block:: python

   # server.py
   from mcp.server.fastmcp import FastMCP

   # Create an MCP server
   mcp = FastMCP("Demo")

   # Add an addition tool
   @mcp.tool()
   def add(a: int, b: int) -> int:
       """Add two numbers"""
       return a + b

   # Add a dynamic greeting resource
   @mcp.resource("greeting://{name}")
   def get_greeting(name: str) -> str:
       """Get a personalized greeting"""
       return f"Hello, {name}!"

Server with Lifespan
------------------

You can add lifespan support for managing startup/shutdown with strong typing:

.. code-block:: python

   from contextlib import asynccontextmanager
   from collections.abc import AsyncIterator
   from dataclasses import dataclass

   from fake_database import Database  # Replace with your actual DB type

   from mcp.server.fastmcp import Context, FastMCP

   @dataclass
   class AppContext:
       db: Database

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


   # Access type-safe lifespan context in tools
   @mcp.tool()
   def query_db(ctx: Context) -> str:
       """Tool that uses initialized resources"""
       db = ctx.request_context.lifespan_context["db"]
       return db.query()

Resources
--------

Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My Application")

   @mcp.resource("config://app")
   def get_config() -> str:
       """Static configuration data"""
       return "App configuration here"

   @mcp.resource("users://{user_id}/profile")
   def get_user_profile(user_id: str) -> str:
       """Dynamic user data"""
       return f"Profile data for user {user_id}"

Resources support different return types:

- ``str``: Plain text
- ``bytes``: Binary data
- ``dict``: JSON data
- ``Image``: Image data with automatic format handling
- Tuple of ``(data, mime_type)``: Custom MIME type

Tools
-----

Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects:

.. code-block:: python

   import httpx
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My Application")

   @mcp.tool()
   def calculate_bmi(weight_kg: float, height_m: float) -> float:
       """Calculate BMI given weight in kg and height in meters"""
       return weight_kg / (height_m**2)

   @mcp.tool()
   async def fetch_weather(city: str) -> str:
       """Fetch current weather for a city"""
       async with httpx.AsyncClient() as client:
           response = await client.get(f"https://api.weather.com/{city}")
           return response.text

Complex Input with Pydantic
^^^^^^^^^^^^^^^^^^^^^^^

FastMCP supports complex input types using Pydantic models:

.. code-block:: python

   from pydantic import BaseModel, Field
   from typing import Annotated
   from mcp.server.fastmcp import FastMCP

   # Define a complex input type
   class ShrimpTank(BaseModel):
       class Shrimp(BaseModel):
           name: Annotated[str, Field(max_length=10)]

       shrimp: list[Shrimp]

   mcp = FastMCP("Shrimp Manager")

   @mcp.tool()
   def name_shrimp(
       tank: ShrimpTank,
       # You can use pydantic Field in function signatures for validation
       extra_names: Annotated[list[str], Field(max_length=10)],
   ) -> list[str]:
       """List all shrimp names in the tank"""
       return [shrimp.name for shrimp in tank.shrimp] + extra_names

Prompts
------

Prompts are reusable templates that help LLMs interact with your server effectively:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP
   from mcp.server.fastmcp.prompts import base

   mcp = FastMCP("My Application")

   @mcp.prompt()
   def review_code(code: str) -> str:
       return f"Please review this code:\n\n{code}"

   @mcp.prompt()
   def debug_error(error: str) -> list[base.Message]:
       return [
           base.UserMessage("I'm seeing this error:"),
           base.UserMessage(error),
           base.AssistantMessage("I'll help debug that. What have you tried so far?"),
       ]

Images
-----

FastMCP provides an ``Image`` class that automatically handles image data:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP, Image
   from PIL import Image as PILImage

   mcp = FastMCP("My Application")

   @mcp.tool()
   def create_thumbnail(image_path: str) -> Image:
       """Create a thumbnail from an image"""
       img = PILImage.open(image_path)
       img.thumbnail((100, 100))
       return Image(data=img.tobytes(), format="png")

   @mcp.tool()
   def load_image(path: str) -> Image:
       """Load an image from disk"""
       # FastMCP handles reading and format detection
       return Image(path=path)

Images can be used as the result of both tools and resources.

Context
------

The Context object gives your tools and resources access to MCP capabilities:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP, Context

   mcp = FastMCP("My Application")

   @mcp.tool()
   async def long_task(files: list[str], ctx: Context) -> str:
       """Process multiple files with progress tracking"""
       for i, file in enumerate(files):
           ctx.info(f"Processing {file}")
           await ctx.report_progress(i, len(files))
           
           # Read another resource if needed
           data = await ctx.read_resource(f"file://{file}")
           
       return "Processing complete"

The Context object provides:

- Progress reporting through ``report_progress()``
- Logging via ``debug()``, ``info()``, ``warning()``, and ``error()``
- Resource access through ``read_resource()``
- Request metadata via ``request_id`` and ``client_id``

Running Your Server
-----------------

There are three main ways to run your FastMCP server:

Development Mode
^^^^^^^^^^^^^^^

For building and testing, use the MCP Inspector:

.. code-block:: bash

   mcp dev server.py

This launches a web interface where you can:

- Test your tools and resources interactively
- See detailed logs and error messages
- Monitor server performance
- Set environment variables for testing

During development, you can:

.. code-block:: bash

   # Add dependencies
   mcp dev server.py --with pandas --with numpy

   # Mount local code for live updates
   mcp dev server.py --with-editable .

Claude Desktop Integration
^^^^^^^^^^^^^^^^^^^^^^^^

For regular use, install in Claude Desktop:

.. code-block:: bash

   mcp install server.py

Your server will run in an isolated environment with:

.. code-block:: bash

   # Custom name
   mcp install server.py --name "My Analytics Server"

   # Environment variables (individual)
   mcp install server.py -e API_KEY=abc123 -e DB_URL=postgres://...

   # Environment variables (from file)
   mcp install server.py -f .env

Direct Execution
^^^^^^^^^^^^^^

For advanced scenarios like custom deployments:

.. code-block:: python

   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My App")

   if __name__ == "__main__":
       mcp.run()

Run it with:

.. code-block:: bash

   # Using the MCP CLI
   mcp run server.py

   # Or with Python/uv directly
   python server.py
   uv run python server.py

Server Object Names
^^^^^^^^^^^^^^^^

All MCP commands will look for a server object called ``mcp``, ``app``, or ``server`` in your file. For custom object names:

.. code-block:: bash

   # Using a standard name
   mcp run server.py

   # Using a custom name
   mcp run server.py:my_custom_server

Mounting to an Existing ASGI Server
---------------------------------

You can mount the SSE server to an existing ASGI server using the ``sse_app`` method:

.. code-block:: python

   from starlette.applications import Starlette
   from starlette.routing import Mount, Host
   from mcp.server.fastmcp import FastMCP

   mcp = FastMCP("My Application")

   # Mount the SSE server to the existing ASGI server
   app = Starlette(
       routes=[
           Mount('/', app=mcp.sse_app()),
       ]
   )

   # or dynamically mount as host
   app.router.routes.append(Host('mcp.acme.corp', app=mcp.sse_app()))

Low-Level Server API
------------------

For more control, you can use the low-level Server API:

.. code-block:: python

   from contextlib import asynccontextmanager
   from collections.abc import AsyncIterator

   from mcp.server import Server
   import mcp.types as types

   # Lifecycle management
   @asynccontextmanager
   async def server_lifespan(server: Server) -> AsyncIterator[dict]:
       # Initialize resources on startup
       db = await Database.connect()
       try:
           yield {"db": db}
       finally:
           # Clean up on shutdown
           await db.disconnect()

   # Create a server with a name and lifespan
   server = Server("example-server", lifespan=server_lifespan)

   # Access lifespan context in handlers
   @server.call_tool()
   async def query_db(name: str, arguments: dict) -> list:
       ctx = server.request_context
       db = ctx.lifespan_context["db"]
       return await db.query(arguments["query"])

Best Practices
------------

1. **Descriptive Names**: Use clear, descriptive names for resources, tools, and prompts
2. **Comprehensive Documentation**: Provide detailed descriptions so models know when and how to use your primitives
3. **Error Handling**: Handle errors gracefully and return meaningful error messages
4. **Type Hints**: Use Python type hints to ensure correct parameter types
5. **Resource Schemas**: Use URL patterns that represent the data hierarchy logically
6. **Security**: Validate inputs and limit access to sensitive operations
7. **Strong Typing**: Use dataclasses and type annotations for lifecycle context
8. **Testability**: Use the MCP Inspector to test your server during development
9. **Environment Management**: Handle environment variables and dependencies properly
10. **Appropriate Return Types**: Choose the right return type for each resource and tool 