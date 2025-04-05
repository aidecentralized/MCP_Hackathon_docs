Building MCP Clients
=================

This guide covers how to build MCP clients using the Python SDK. Clients can connect to MCP servers, discover capabilities, and interact with resources, tools, and prompts.

Client Session
------------

The SDK provides a high-level client interface for connecting to MCP servers. The main entry point is the ``ClientSession`` class:

.. code-block:: python

   from mcp import ClientSession, StdioServerParameters, types
   from mcp.client.stdio import stdio_client

   # Create server parameters for stdio connection
   server_params = StdioServerParameters(
       command="python",  # Executable
       args=["example_server.py"],  # Optional command line arguments
       env=None,  # Optional environment variables
   )

   # Optional: create a sampling callback
   async def handle_sampling_message(
       message: types.CreateMessageRequestParams,
   ) -> types.CreateMessageResult:
       return types.CreateMessageResult(
           role="assistant",
           content=types.TextContent(
               type="text",
               text="Hello, world! from model",
           ),
           model="gpt-3.5-turbo",
           stopReason="endTurn",
       )

   async def run():
       async with stdio_client(server_params) as (read, write):
           async with ClientSession(
               read, write, sampling_callback=handle_sampling_message
           ) as session:
               # Initialize the connection
               await session.initialize()

               # Use session methods...

Connection Methods
---------------

There are different ways to connect to MCP servers:

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

Working with Prompts
-----------------

Discover and use prompts from the server:

.. code-block:: python

   # List available prompts
   prompts = await session.list_prompts()
   print(f"Available prompts: {prompts}")
   
   # Get a prompt
   prompt = await session.get_prompt(
       "example-prompt", arguments={"arg1": "value"}
   )
   print(f"Prompt: {prompt}")

Working with Resources
-------------------

Discover and read resources from the server:

.. code-block:: python

   # List available resources
   resources = await session.list_resources()
   print(f"Available resources: {resources}")
   
   # Read a resource
   content, mime_type = await session.read_resource("file://some/path")
   print(f"Resource content ({mime_type}): {content}")
   
   # Subscribe to resource list changes
   async for resources in session.subscribe_resources():
       print(f"Resources updated: {resources}")

Working with Tools
---------------

Discover and call tools on the server:

.. code-block:: python

   # List available tools
   tools = await session.list_tools()
   print(f"Available tools: {tools}")
   
   # Call a tool
   result = await session.call_tool(
       "tool-name", 
       arguments={"arg1": "value"}
   )
   print(f"Tool result: {result}")

Message Creation
--------------

MCP clients can handle message creation for AI models:

.. code-block:: python

   from mcp import types
   
   # Define a sampling callback
   async def handle_sampling_message(
       message: types.CreateMessageRequestParams,
   ) -> types.CreateMessageResult:
       # This is where you would call your LLM API
       return types.CreateMessageResult(
           role="assistant",
           content=types.TextContent(
               type="text",
               text="Generated response from the model",
           ),
           model="gpt-4",
           stopReason="endTurn",
       )
   
   # Create a session with the sampling callback
   async with ClientSession(
       read, write, sampling_callback=handle_sampling_message
   ) as session:
       # Now the session can handle message creation requests

Error Handling
------------

Handle errors from the MCP server:

.. code-block:: python

   from mcp.exceptions import MCPError, ResourceNotFoundError
   
   try:
       content, mime_type = await session.read_resource("file://nonexistent.txt")
   except ResourceNotFoundError as e:
       print(f"Resource not found: {e}")
   except MCPError as e:
       print(f"MCP error: {e}")

Integration with LLMs
------------------

Integrating MCP with LLM frameworks:

.. code-block:: python

   # Example with LlamaIndex
   from llama_index.core import Settings, VectorStoreIndex
   from llama_index.core.tools import FunctionTool
   from llama_index.llms.openai import OpenAI
   
   # Create OpenAI LLM
   llm = OpenAI(model="gpt-4")
   Settings.llm = llm
   
   # List tools from MCP server
   tools = await session.list_tools()
   
   # Convert MCP tools to LlamaIndex tools
   llamaindex_tools = []
   for tool in tools:
       async def tool_fn(**kwargs):
           return await session.call_tool(tool.name, arguments=kwargs)
       
       llamaindex_tools.append(FunctionTool.from_defaults(
           name=tool.name,
           description=tool.description,
           fn=tool_fn,
       ))
   
   # Use tools with LlamaIndex agent
   agent = OpenAIAgent.from_tools(llamaindex_tools, llm=llm)
   response = await agent.chat("Can you search for information about X?")

Best Practices
------------

1. **Handle Reconnection**: Implement reconnection logic for network failures
2. **Graceful Degradation**: Handle missing capabilities gracefully
3. **Resource Caching**: Cache resources to reduce repeated requests
4. **Type Checking**: Validate arguments before sending to the server
5. **Security**: Always validate and sanitize data received from servers 